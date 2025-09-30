import urllib
from urllib.request import Request, urlopen
from random import choice, randint
import re
from time import sleep

# Example user agents (add more if you like)
agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
]


def create_request(url):
    headers = {"User-Agent": choice(agents)}
    req = Request(url, data=None, headers=headers)
    return req


def fetch(url):
    try:
        response = urlopen(create_request(url), timeout=10)
        if response.getcode() == 200:
            data = response.read()
            return data
        else:
            return None
    except:
        return None


import re


from urllib.parse import urljoin

from urllib.parse import urljoin

def extract_links(html, base_url=""):
    try:
        html = str(html)  # ensure string type
        raw_links = re.findall(r'href=[\'"]?([^\'" >]+)', html)
        links = []
        for link in raw_links:
            if link.startswith("//"):  # protocol-relative
                link = "http:" + link
            elif not link.startswith("http"):  # relative path
                if base_url:
                    link = urljoin(base_url, link)
                else:
                    continue
            links.append(link)
        return list(set(links))  # deduplicate
    except Exception as e:
        print(f"Error extracting links: {e}")
        return []


def crawl(start_url, steps):
    queue = [start_url]
    crawled = []
    for _ in range(steps):
        try:
            url = choice(queue)
            queue.remove(url)
            html = fetch(url)
            if html:
                queue = list(set(queue + extract_links(html, url)))
            crawled.append(url)
            sleep(5 + randint(0, 10))  # required delay per assignment
        except Exception as e:
            print(f"Error during crawl step: {e}")
            pass
    return crawled

