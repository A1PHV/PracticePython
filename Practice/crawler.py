#!/usr/bin/env python

import requests

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = ""
with open("", "r") as wlf:
    for line in wlf:
        word = line.strip()
        test_url = word + "." + target_url
        response = request(test_url)
        if "200" in response:
            print("[+] Exist Domain: ", test_url)
