import tracert
import crawl
import socket
import json
from urllib.parse import urlparse

STARTING_URL = 'http://www.python.org'
STEPS = 10
OUTPUT = {}
OUTFILE = 'netdata.json'

print("Crawling...")
urls = crawl.crawl(STARTING_URL, STEPS)

print("Crawling complete...Tracing")
for url in urls :
    try:
        print("Tracing: " + url)
        url_parts = urlparse(url)
        addr = socket.gethostbyname(url_parts.netloc)
        route = tracert.trace(addr)
        previous = None
        for ip in route:
            if ip in OUTPUT:
                OUTPUT[ip]['url'].append(url)
                OUTPUT[ip]['url'] = list(set(OUTPUT[ip]['url']))
            else:
                OUTPUT[ip] = {'asn' : None, 'links' : [], 'url' : [url]}
            if previous:
                OUTPUT[previous]['links'].append(ip)
                OUTPUT[ip]['links'].append(previous)
                OUTPUT[ip]['links'] = list(set(OUTPUT[ip]['links']))
                OUTPUT[previous]['links'] = list(set(OUTPUT[previous]['links']))
            previous = ip
            if not OUTPUT[ip]['asn']:
                asn_data = tracert.asn(ip)
                OUTPUT[ip]['asn'] = asn_data
    except:
        print("Failed to trace: " + url)
        pass


with open(OUTFILE, 'a+') as f:
    f.write(json.dumps(OUTPUT, indent=4, sort_keys = True))