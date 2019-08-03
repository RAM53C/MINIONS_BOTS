from lxml.html import fromstring
import requests
from itertools import cycle
import traceback

def get_proxies():
    print("Setting up new proxies...")
    file = open("list.txt", "r")
    proxlist = [];
    for line in file:
        proxlist.append(line.replace('\n',''))
    return proxlist


#If you are copy pasting proxy ips, put in the list below
#proxies = ['121.129.127.209:80', '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128', '13.92.196.150:8080']
proxies = get_proxies()
print(str(len(proxies)) + " Proxies Loaded")
proxy_pool = cycle(proxies)

url = 'https://httpbin.org/ip'
print("Testing Proxies...");
proxfile = open("validatedProxies.txt", "w+")
for i in range(1,len(proxies)):
    #Get a proxy from the pool
    proxy = next(proxy_pool)
    print("Request #%d"%i)
    try:
        response = requests.get(url,timeout=8,proxies={"http": proxy, "https": proxy})
        print(response.json())
        #Request worked
        proxfile.write(str(proxy) + "\n");
    except:
        #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
        #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
        print("Skipping. Connnection error")
proxfile.close();
