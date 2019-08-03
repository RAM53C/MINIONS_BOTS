from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
import urllib.request

def get_proxies():
    #print("Loading proxies...")
    file = open("validatedProxies.txt", "r")
    proxlist = [];
    for line in file:
        proxlist.append(line.replace('\n',''))
    return proxlist


#If you are copy pasting proxy ips, put in the list below
#proxies = ['121.129.127.209:80', '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128', '13.92.196.150:8080']
proxies = get_proxies()
print(str(len(proxies)) + " Proxies Loaded")
proxy_pool = cycle(proxies)

url = 'https://www.off---white.com/en/PT'
#print("Testing Link...");
for i in range(1,len(proxies)):
    #Get a proxy from the pool
    proxy = next(proxy_pool)
    print("Request #%d"%i)
    try:
        page = requests.get(url, proxies={"http": proxy, "https": proxy})
        print(page.response)
        print("")
    except Exception as e:
        #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
        #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
        print("Skipping. Connnection error")
        print("Error: " + str(e))
