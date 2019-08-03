from selenium import webdriver
from config import keys
import time
import random
import re

def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        print((endTime - startTime)/1000, 's')
        return result
    return wrapper

# will cookies improve load time?
#options = webdriver.ChromeOptions()
#options.add_argument('user-data-dir=www.supremenewyork.com')

'''
def order():
    # add to cart
    driver.find_element_by_name('commit').click()

    # wait for checkout button element to load
    time.sleep(.5)
    checkout_element = driver.find_element_by_class_name('checkout')
    checkout_element.click()

    # fill out checkout screen fields
    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(keys['name'])
    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(keys['email'])
    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(keys['phone_number'])
    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(keys['street_address'])
    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(keys['zip_code'])
    driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(keys['city'])
    driver.find_element_by_xpath('//*[@id="orcer"]').send_keys(keys['card_cvv'])
    driver.find_element_by_id('nnaerb').send_keys(keys['card_number'])


    process_payment = driver.find_element_by_xpath('//*[@id="pay"]/input')
    process_payment.click()
'''
def newRequest():
    #Load Categories
    traficCAT = keys['trafic_rn'];
    # Random choice
    CAT = random.choice(traficCAT);
    print("RANDOM REQUEST: " + str(CAT))
    chrome.get(CAT)
    #Create Products list
    p_models = [];
    products = chrome.find_elements_by_class_name("product")
    for product in products:
        productlink = product.find_element_by_tag_name("a")
        INhtml = str(productlink.get_attribute('innerHTML'))
        regex = r"(?<=alt=).*?(?= image)"
        x = re.findall(regex, INhtml)[0].replace('"', "");
        p_models.append(x.lower())
    print(p_models)

def getProducts():
    #Get all products
    products = chrome.find_elements_by_class_name("product")
    for product in products:
        productlink = product.find_element_by_tag_name("a")
        print("Product link struct: " + str(productlink.get_attribute('innerHTML')))

if __name__ == '__main__':
    # load chrome with proxy
    '''
    PROXY = "173.233.55.120:443" # IP:PORT or HOST:PORT

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    '''
    chrome = webdriver.Chrome()
    #We need random navigation
    # get product url
    print ("PAGE SOURCE!!")
    print("=====================================================")
    #chrome.get(keys['product_url'])
    #getProducts()
    print("=====================================================")
    time.sleep(2)
    #Now do some random trafic
    request = newRequest();
