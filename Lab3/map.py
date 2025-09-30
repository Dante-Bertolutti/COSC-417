import tracert_mod
import crawl
import socket
import json
from urllib.parse import urlparse

STARTING_URL = 'https://en.wikipedia.org/wiki/Special:Random'
STEPS = 100
OUTPUT = {}
OUTFILE = 'netdata.json'

print("Crawling...")
urls = crawl.crawl(STARTING_URL, STEPS)

print("Crawling complete...Tracing")
for url in urls:
    try:
        print("Tracing:", url)
        url_parts = urlparse(url)
        if not url_parts.netloc:  # skip invalid/relative links
            raise ValueError(f"Invalid URL (no host): {url}")
        addr = socket.gethostbyname(url_parts.netloc)
        route = tracert_mod.trace(addr)   # <- updated
        if not route:
            raise ValueError(f"No traceroute returned for {addr}")
        previous = None
        for ip in route:
            if ip not in OUTPUT:
                OUTPUT[ip] = {'asn': None, 'links': [], 'url': [url]}
            else:
                OUTPUT[ip]['url'].append(url)
                OUTPUT[ip]['url'] = list(set(OUTPUT[ip]['url']))
            if previous:
                OUTPUT[previous]['links'].append(ip)
                OUTPUT[ip]['links'].append(previous)
                OUTPUT[ip]['links'] = list(set(OUTPUT[ip]['links']))
                OUTPUT[previous]['links'] = list(set(OUTPUT[previous]['links']))
            previous = ip
            if not OUTPUT[ip]['asn']:
                OUTPUT[ip]['asn'] = tracert_mod.asn(ip)   # <- updated
    except Exception as e:
        print(f"Failed to trace {url}: {e}")
        continue

print("OUTPUT so far:", json.dumps(OUTPUT, indent=2))

with open(OUTFILE, 'a+') as f:
    f.write(json.dumps(OUTPUT, indent=4, sort_keys=True))
