from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import json
import threading
import subprocess
import time
import sys
import os

def cnf_parser(): #Refresh time: 1 second
    global keys
    global working
    print("Loading Parser...")
    cp = threading.currentThread()
    while getattr(cp, "do_run", True):
        config_file = open('config.json')
        keys = json.load(config_file)
        if keys["MINshop"] == "shutdown":
            stop_shop();
        #Conditions
        time.sleep(1)

def update_cnf(cnf):
    myCmd = 'python cnf_modifier.py -c "' + str(cnf) + '"'
    print("Updating Config: " + str(myCmd))
    os.system(myCmd)

def stop_shop():
    global working
    print("Parser recieved shutdown")
    print("Stopping MainBuy...")
    working = False
    stop_parser();
    sys.exit(1)

def stop_parser():
    global cpw
    cpw.do_run = False
    sys.exit(1)

def setup():
    global driver
    driver = webdriver.Chrome();

def requestLink(link):
    global driver
    print("Requesting: " + link)
    driver.get(link)
    assert "Supreme" in driver.title
    print("Done!")

def MainBuy():
    global keys
    global working
    print("Waiting for products...")
    working = True
    while working:
        products = keys["toBUY"]
        if products:
            print("Products found, waiting 5 seconds to get more...")
            time.sleep(5) #Wait 5 seconds for more products
            products = keys["toBUY"]
            for key, value in products.items():
                models = keys["toBUY"][key]
                link = key
                print("Product: " + key)
                for key, value in models.items():
                    buyProduct(link, key, value, models);
                    break
            # Finished, proceed to checkout
            print("--> Checkout")
            Checkout();
            print("Waiting for products...")
    print("MainBuy: SHUTDOWN")

def buyProduct(link, key, value, models):
    global keys
    # Get Product Page
    print("Size to buy: " + key)
    requestLink(link);
    addToCart(key);
    # After buy
    #Get Key value
    qnty = int(value) - 1
    if qnty == 0:
        del models[key]
    else:
        models[key] = qnty
    if not models:
        print("Stock to buy: Complete")
        print("Deleting link...")
        toBuy = keys["toBUY"] # Parse Buy List
        del toBuy[link] # Remove link from Buy List
        cnfdict = {"toBUY": toBuy}
        update_cnf(cnfdict)
    else:
        toBuy = keys["toBUY"] # Parse Buy List
        toBuy[link] = models
        cnfdict = {"toBUY": toBuy}
        update_cnf(cnfdict)

def addToCart(size):
    global driver
    # First Check Size
    if size != "NA":
        # Size is defined, check correct size option
        select = Select(driver.find_element_by_name('size')) # Get select element
        select.select_by_visible_text(size)
    time.sleep(1)
    driver.find_element_by_name("commit").click()
    time.sleep(1)


def Checkout():
    global driver
    print("Requesting checkout page...")
    time.sleep(2)
    requestLink("https://www.supremenewyork.com/checkout")
    # Load checkout info
    print("Reading Account File...")
    config_file = open('account.json')
    ac = json.load(config_file)
    # Fill form
    for key, value in ac.items():
        if key in ["order_billing_country", "credit_card_type", "credit_card_month", "credit_card_year"]:
            select = Select(driver.find_element_by_id(key)) # Get select element
            select.select_by_visible_text(value)
        elif key == "order_terms":
            checkboxes = [];
            checkboxes = driver.find_elements_by_class_name("iCheck-helper");
            terms_checkbox = checkboxes[-1]
            terms_checkbox.click();
        else:
            element = driver.find_element_by_id(key)
            element.send_keys(value)
    print("Processing Payment...")



if __name__ == '__main__':
    global cpw
    global threads
    global keys
    setup();
    threads = []
    cpw = threading.Thread(target=cnf_parser);
    cpw.start();
    time.sleep(2)
    MainBuy();
