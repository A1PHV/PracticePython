#!/usr/bin/env python
import re
import requests
import urlparse

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = ""
target_links = []

def extract_links_from(url):
    response = request(target_url)
    return re.findall('(?:href=")(.*?)"', response.content)
def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]
        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)
crawl(target_url)