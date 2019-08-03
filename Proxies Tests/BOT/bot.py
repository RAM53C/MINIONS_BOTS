from selenium import webdriver
from config import keys
import time
import random
import re

def newRequest():
    #Load Categories
    traficCAT = keys['trafic_rn'];
    # Random choice
    CAT = random.choice(traficCAT);
    print("RANDOM REQUEST: " + str(CAT))
    #Get link



    #Create Products list from raw html
    p_models = [];
    products = chrome.find_elements_by_class_name("product")
    for product in products:
        productlink = product.find_element_by_tag_name("a")
        INhtml = str(productlink.get_attribute('innerHTML'))
        regex = r"(?<=alt=).*?(?= image)"
        x = re.findall(regex, INhtml)[0].replace('"', "");
        p_models.append(x.lower())
    print(p_models)


if __name__ == '__main__':
    
    request = newRequest();
