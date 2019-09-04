import json
from bs4 import BeautifulSoup
import time
import random
import string
import re
import datetime
import threading
import subprocess
import sys
import os
import requests
import numpy as np
global i
global pmodelsset
global products_math
global p_models
global keys
global threads
global working
#For Links Setup
global linkcheck
global ready
i = 0
working = False
pmodelsset = False
keysdefined = False
linkcheck = False
ready = False

# Enable/Disable Console Logs
logs = True

def logToConsole(text):
    if logs == True:
        print(text)
        sys.stdout.flush()

# Check Internet Connection
# @yasinkuyu 08/09/2017

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


#BOT Parser
def cnf_parser(): #Refresh time: 1 second
    global keys
    logToConsole("Loading Parser...")
    cp = threading.currentThread()
    while getattr(cp, "do_run", True):
        config_file = open('config.json')
        keys = json.load(config_file)
        #Conditions
        cnf_process(keys)
        time.sleep(1)

def update_cnf(cnf):
    myCmd = 'python cnf_modifier.py -c "' + str(cnf) + '"'
    logToConsole("Updating Config: " + str(myCmd))
    os.system(myCmd)

def removeProduct(link):
    global keys
    buylinks = keys["product_url"];
    print("Product was aquired, removing link from list...")
    if link in buylinks:
        buylinks.remove(link)
        # Remove product link from list
        cnfdict = {"product_url": buylinks}
        update_cnf(cnfdict)
    if not buylinks: #Check if array is empty
        print("Bot finished, no links to check")
        cnfdict = {"state": "stop"}
        update_cnf(cnfdict)



def cnf_process(keys):
    global oldkeys
    global keysdefined
    global linkcheck
    global ready
    global working
    if (keysdefined == True and oldkeys != keys) or keysdefined == False:
        oldkeys = keys
        if keys["state"] == "shutdown" and keysdefined == True:
            logToConsole("Parser recieved shutdown")
            global cpw
            cpw.do_run = False
            sys.exit(1)
        if keysdefined == False:
            logToConsole("Parser state value is " + keys["state"] + " but its the first time, changing state")
            cnfdict = {"state": "unset"}
            update_cnf(cnfdict)
        if keys["state"] == "unset":
            logToConsole("Link Unset, waiting for control console...")
        if keys["state"] == "check":
            linkcheck = check_links(keys);
        if keys["state"] == "ready":
            if linkcheck:
                linkcheck = False
                ready = True
                logToConsole("Ready - waiting for console")
            else:
                logToConsole("Error - Links not checked")
                cnfdict = {"state": "unset"}
                update_cnf(cnfdict)
        if keys["state"] == "start":
            if ready == True:
                #Init BOT
                ready = False
                logToConsole("Initializing BOT...")
                cnfdict = {"state": "working"}
                update_cnf(cnfdict);
                initialize_bot();
            else:
                logToConsole("Error while starting: State <ready> required")
                cnfdict = {"state": "unset"}
                update_cnf(cnfdict)
        if keys["state"] == "stop":
            if working == True:
                #Stop BOT
                logToConsole("Stopping BOT...")
                linkcheck = True
                stop_bot();
                cnfdict = {"state": "ready"}
                update_cnf(cnfdict);
            else:
                logToConsole("Error while stoping: State <working> not defined")
                cnfdict = {"state": "unset"}
                update_cnf(cnfdict)
        #Code for keysdefined
        if keysdefined == False:
            keysdefined = True
        #####################

def check_links(keys):
    logToConsole("Checking Links...")
    #Validate links
    buylinks = keys["product_url"];
    if buylinks:
        blv = []
        rpl = []
        for link in buylinks: # Just check domain
            if ("https://www.supremenewyork.com/shop" in link):
                logToConsole(str(link) + " OK!")
                blv.append(link)
            else:
                logToConsole(str(link) + " FAILED!")
                rpl.append(link)
        if (blv):
            #Export BLV and create config
            cnfdict = {"product_url": blv, "rejected_links": rpl, "state": "ready"}
            update_cnf(cnfdict)
            return True
        else:
            #Export BLV and create config
            cnfdict = {"product_url": blv, "rejected_links": rpl, "state": "unset"}
            update_cnf(cnfdict)
            return False
    else:
        logToConsole("No Links to check")
        cnfdict = {"state": "unset"}
        update_cnf(cnfdict)
        return False

def initialize_bot():
    global working
    if working == True:
        logToConsole("BOT Instance already running")
        logToConsole("Set state to <stop> first")
    else:
        working = True
        global threads
        global bw
        bw = threading.Thread(target=MainCheck);
        bw.start();

def stop_bot():
    global bw
    global working
    bw.do_run = False
    working = False

def setup():
    global searchbar
    searchbar = [];
    logToConsole("CHECK_CONNECTION")
    if check_internet:
        logToConsole("CONNECTED")
    else:
        logToConsole("CONNECTION_ERROR")
        logToConsole("Failed to connect")
        os.system("python cnf_modifier.py -c \"{'state':'shutdown'}\"")
        sys.exit(1)

def loadLink(link):
    r = requests.get(link)
    page_html = r.text;
    soup = BeautifulSoup(page_html, "html.parser")
    productname = soup.find_all('h1', {'class':"protect"})[0];
    productname = str(productname.contents[0]);
    productstate = soup.find_all('fieldset', {'id':"add-remove-buttons"})[0];
    productstate = productstate.findChildren("input" , recursive=False)
    productprice = soup.find_all('p', {'class':"price"})[0];
    productprice = productprice.findChildren("span" , recursive=False)[0];
    productprice = str(productprice.contents[0]);
    sizes = []
    if productstate:
        product_available = True
        # Get available sizes
        productsizes = soup.find_all('option'); #WARNING: Parameter should be more specific
        if productsizes:
            for size in productsizes:
                size = str(size.contents[0]);
                sizes.append(size)
    else:
        product_available = False
    product = {
    "name": productname,
    "state": product_available,
    "price": productprice,
    "sizes": sizes
    }
    return product


def LinkRequest(link):
    global keys
    #Get link
    product = loadLink(str(link))
    #Strip Link
    if (product["state"]):
        ConsoleProductLog(product["name"], "Available for buy", product["sizes"])
        # Check Sizes
        sizeconfig = keys["buyoptions"][link];
        buysizes = {}
        for size in product["sizes"]:
            if size in sizeconfig:
                # Get sizes
                buysizes[size] = sizeconfig[size]
        if buysizes or "NA" in sizeconfig:
            if "NA" in sizeconfig:
                buysizes = sizeconfig
            print("Buying Stocks...")
            # Generate order code
            ordercode = genCode(str(link));
            buyProduct(link, product["name"], product["price"], buysizes, keys["id"], ordercode);
            removeProduct(link)
    else:
        ConsoleProductLog(product["name"], "Not Available", product["sizes"])
    time.sleep(1)

def ConsoleProductLog(product, state, sizes):
    now = datetime.datetime.now()
    print("=========================")
    print("Product: " + str(product))
    print("State: " + str(state))
    if sizes:
        print("Available Sizes: " + str(sizes))
    print("Checked at: " + now.strftime("%H:%M:%S"))
    print("=========================")


def MainCheck():
    global keys
    logToConsole("BOT: Starting...")
    bws = threading.currentThread()
    while getattr(bws, "do_run", True):
        buylinks = keys["product_url"];
        for link in buylinks:
            LinkRequest(link); #Link Request

def genCode(link):
    # Generate 6 chars bot code
    bcode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    # Grab product code
    pcode = link.split("/")[-1]
    # Final code
    ocode = str(pcode) + "-" + str(bcode)
    return ocode;

def buyProduct(link, name, price, size, botid, ordercode):
    # Create Invoice
    OrderInvoice(link, name, price, size, botid, ordercode);
    # Add to buy products
    cnfdict = {"toBUY": { link: size}}
    update_cnf(cnfdict)

def OrderInvoice(link, name, price, size, botid, ordercode):
    print("Creating Invoice...")
    print("")
    print("")
    print("*********************")
    print("Order Info:")
    print("*********************")
    print("Order Code: " + str(ordercode))
    print("Product Name: " + str(name))
    print("Product Link: " + str(link))
    print("Quantity: ")
    total = 0
    price = price.replace("€", "")
    for key, value in size.items():
        print(" - " + key + ": " + str(value) + " x " + str(price) + "€")
        total += value * int(price)
    print(" Total: " + str(total) + "€")
    print("Buy Method: MIN-IONS Shop Gateway (MINshop.py)")
    print("")
    now = datetime.datetime.now()
    print("Processed by " + botid + " at " + now.strftime("%m/%d/%Y, %H:%M:%S"))
    print("")
    print("")
    # Write on file
    f = open("invoices/"+str(ordercode)+".txt", "w+");
    f.write("*********************\n")
    f.write("Order Info:\n")
    f.write("*********************\n")
    f.write("Order Code: " + str(ordercode) + "\n")
    f.write("Product Name: " + str(name) + "\n")
    f.write("Product Link: " + str(link) + "\n")
    f.write("Quantity: " + "\n")
    for key, value in size.items():
        f.write(" - " + key + ": " + str(value) + " x " + str(price) + "€" + "\n")
    f.write(" Total: " + str(total) + "€" + "\n")
    f.write("Buy Method: MIN-IONS Shop Gateway (MINshop.py)" + "\n")
    f.write("" + "\n")
    f.write("Processed by " + botid + " at " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
    f.close();
    print("Invoice saved at invoices/"+str(ordercode)+".txt")



if __name__ == '__main__':
    setup();
    global cpw
    global threads
    threads = []
    cpw = threading.Thread(target=cnf_parser);
    cpw.start();
