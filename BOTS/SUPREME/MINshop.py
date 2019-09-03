from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import threading
import subprocess
import time
import sys
import os

def cnf_parser(): #Refresh time: 1 second
    global keys
    print("Loading Parser...")
    cp = threading.currentThread()
    while getattr(cp, "do_run", True):
        config_file = open('config.json')
        keys = json.load(config_file)
        #Conditions
        time.sleep(1)

def update_cnf(cnf):
    myCmd = 'python cnf_modifier.py -c "' + str(cnf) + '"'
    logToConsole("Updating Config: " + str(myCmd))
    os.system(myCmd)

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

def MainBuy(link):
    products = keys["toBUY"]
    for key, value in products.items():
        models = keys["toBUY"][key]
        print("Product: " + key)
        for key, value in models.items():
            buyProduct(link, key, value, models);
            break
    # Finished, proceed to checkout
    print("--> Checkout")

def buyProduct(link, key, value, models):
    # Get Product Page
    print("Size to buy: " + key)
    requestLink(link);



    # After buy
    #Get Key value
    qnty = int(value) - 1
    if qnty == 0:
        del models[key]
    else:
        models[key] = qnty
    cnfdict = {"toBUY": { link: models}}
    update_cnf(cnfdict)

if __name__ == '__main__':
    global cpw
    global threads
    global keys
    try:
        setup();
        threads = []
        cpw = threading.Thread(target=cnf_parser);
        cpw.start();
        config_file = open('config.json')
        keys = json.load(config_file)
        link = keys["toBUY"][0];
        MainBuy(link);
    except KeyboardInterrupt:
        print "Bye"
        stop_parser();
        sys.exit(1)
