from config import keys
from imagesearch import *
from bs4 import BeautifulSoup
import time
import random
import re
import pyperclip
import datetime

global i
global pmodelsset
global products_math
global p_models
i = 0
pmodelsset = False

def setup():
    global searchbar
    searchbar = [];
    #Get search bar coordinates
    pos = imagesearch("imagedata/googlesearch.png")
    if pos[0] != -1:
        #Some Maths
        x = pos[0] + 200
        y = pos[1] + 15
        print("Search Bar position : ", x, y)
        searchbar.append(x)
        searchbar.append(y)
    else:
        print("image not found")

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
    #print("Loading Link...")
    # Move to search bar
    pyautogui.moveTo(searchbar[0], searchbar[1])
    pyautogui.click()
    time.sleep(0.5)
    # Type link
    pyperclip.copy(link)
    pyautogui.hotkey('command', 'v')
    pyautogui.press('enter')
    # Check if page was loaded
    #print("Waiting for response...")
    response = waitfor_image(weblogo)
    if response:
        print("Received Response")

def getSource():
    # Get Source Code page
    time.sleep(0.5)
    pyautogui.hotkey('command', 'alt', 'u')
    #print("Waiting for response...")
    response = waitfor_image("imagedata/html.png")
    #if response:
        #print("Received Response")
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
    global i
    global pmodelsset
    global products_math
    global p_models
    if pmodelsset == False:
        #Load Categories
        traficCAT = keys['trafic_rn'];
        # Random choice
        CAT = random.choice(traficCAT);
        print("RANDOM REQUEST: " + str(CAT))
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
        #print(p_models)
        print(str(len(p_models)) + " Products")
        products_math = len(p_models) - random.randint(0, len(p_models) - 1)
        print("Choosing " + str(products_math))
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
    print("Random Link Generated: " + str(randlink))
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
    #print("Screen Size:")
    screensize = pyautogui.size();
    sx = screensize[0]
    sy = screensize[1]
    print("X: " + str(sx) + " | Y: " + str(sy))
    for x in range(0, random.randint(1, 2)):
        tpx = random.randint(0, sx)
        tpy = random.randint(0, sy)
        tftp = random.uniform(0.5, 1)
        #print("Random Moving: STEP: %s | X: %s Y: %s | Motion Time: %s" % (str(x), str(tpx), str(tpy), str(tftp)))
        pyautogui.moveTo(tpx, tpy, tftp)

if __name__ == '__main__':
    #Setup
    setup();
    buylinks = keys["product_url"];
    #Main Program
    for x in range(0,2):
        RandomRequest(); #Random request
        for link in buylinks:
            PointerTrick(); #Confuse Server UPTs (User Pointer Trackers)
            LinkRequest(link); #Link Request
