import json
from imagesearch import *
from bs4 import BeautifulSoup
import time
import random
import re
import pyperclip
import datetime
import threading
import subprocess
import sys
import os
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
            if ("https://www.off---white.com/en/PT/men/products/" in link) or ("https://www.off---white.com/en/PT/women/products/" in link):
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
    bw.do_run = False

def setup():
    global searchbar
    searchbar = [];
    logToConsole("GET_BROWSER")
    #Get search bar coordinates
    pos = imagesearch("imagedata/googlesearch.png")
    if pos[0] != -1:
        #Some Maths
        x = pos[0] + 200
        y = pos[1] + 15
        logToConsole("BAR_FOUND")
        logToConsole(str("Search Bar position : " + str(x) + " " + str(y)))
        searchbar.append(x)
        searchbar.append(y)
    else:
        logToConsole("BAR_NOT_FOUND")
        logToConsole("Failed to get browser: image not found")
        os.system("python cnf_modifier.py -c \"{'state':'shutdown'}\"")
        sys.exit(1)

def waitfor_image(imgname):
    pos = imagesearch_loop(imgname, 0.5)
    return True

def detect_image(imgname):
    pos = imagesearch(imgname)
    if pos[0] != -1:
        return True
    else:
        return False

def loadLink(link, weblogo):
    global searchbar
    #logToConsole("Loading Link...")
    # Move to search bar
    pyautogui.moveTo(searchbar[0], searchbar[1])
    pyautogui.click()
    time.sleep(0.5)
    # Type link
    pyperclip.copy(link)
    pyautogui.hotkey('command', 'v')
    pyautogui.press('enter')
    # Check if page was loaded
    #logToConsole("Waiting for response...")
    response = waitfor_image(weblogo)
    if response:
        logToConsole("Received Response")

def getSource():
    # Get Source Code page
    time.sleep(0.5)
    pyautogui.hotkey('command', 'alt', 'u')
    #logToConsole("Waiting for response...")
    response = waitfor_image("imagedata/html.png")
    #if response:
        #logToConsole("Received Response")
    # Get html
    pyautogui.hotkey('command', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('command', 'c')
    time.sleep(0.5)
    pyautogui.hotkey('command', 'w')
    # Return Clipboard
    time.sleep(1)
    html = pyperclip.paste()
    return html

def innerHTML(element):
    """Returns the inner HTML of an element as a UTF-8 encoded bytestring"""
    return element.encode_contents()

def RandomRequest():
    global keys
    global i
    global pmodelsset
    global products_math
    global p_models
    if pmodelsset == False:
        #Load Categories
        traficCAT = keys['trafic_rn'];
        # Random choice
        CAT = random.choice(traficCAT);
        logToConsole("RANDOM REQUEST: " + str(CAT))
        #Get link
        loadLink(str(CAT), "imagedata/offwhite.png")
        # Get HTML
        page_html = getSource();
        # Parse html
        soup = BeautifulSoup(page_html, "html.parser")
        #Create Products list from raw html
        p_models = [];
        products = soup.find_all('article', {'class':"product"})
        for product in products:
            productlink = str(product.findChildren("a" , recursive=False))
            regex = r"(?<=img alt=).*?(?= image)"
            x = re.findall(regex, productlink)[0].replace('"', "");
            p_models.append(x.lower())
        #logToConsole(p_models)
        logToConsole(str(len(p_models)) + " Products")
        products_math = len(p_models) - random.randint(0, len(p_models) - 1)
        logToConsole("Choosing " + str(products_math))
        pmodelsset = True
    else:
        if i == products_math:
            pmodelsset = False
            i = 0
        else:
            i = i + 1
    #Choose one
    randmodel = random.choice(p_models)
    #Create link
    randlink = "https://www.off---white.com/en/PT/men/products/" + str(randmodel)
    logToConsole("Random Link Generated: " + str(randlink))
    #Get link
    loadLink(str(randlink), "imagedata/offwhite.png")
    i = i + 1

def LinkRequest(link):
    #Get link
    loadLink(str(link), "imagedata/offwhite.png")
    # Get product state (Using OpenCV)
    product_available = detect_image("imagedata/addtocart.png")
    #Strip Link
    product = link.split("/")[-1]
    if (product_available):
        ConsoleProductLog(product, "Available for buy")
    else:
        ConsoleProductLog(product, "Not Available")

def ConsoleProductLog(product, state):
    now = datetime.datetime.now()
    print("=========================")
    print("Product: " + str(product))
    print("State: " + str(state))
    print("Checked at: " + now.strftime("%H:%M:%S"))
    print("=========================")

def PointerTrick():
    #logToConsole("Screen Size:")
    screensize = pyautogui.size();
    sx = screensize[0]
    sy = screensize[1]
    logToConsole("X: " + str(sx) + " | Y: " + str(sy))
    for x in range(0, random.randint(1, 2)):
        tpx = random.randint(0, sx)
        tpy = random.randint(0, sy)
        tftp = random.uniform(0.5, 1)
        #logToConsole("Random Moving: STEP: %s | X: %s Y: %s | Motion Time: %s" % (str(x), str(tpx), str(tpy), str(tftp)))
        pyautogui.moveTo(tpx, tpy, tftp)

def MainCheck():
    global keys
    logToConsole("BOT: Starting...")
    buylinks = keys["product_url"];
    bws = threading.currentThread()
    while getattr(bws, "do_run", True):
        RandomRequest(); #Random request
        for link in buylinks:
            PointerTrick(); #Confuse Server UPTs (User Pointer Trackers)
            LinkRequest(link); #Link Request

if __name__ == '__main__':
    setup();
    global cpw
    global threads
    threads = []
    cpw = threading.Thread(target=cnf_parser);
    cpw.start();
