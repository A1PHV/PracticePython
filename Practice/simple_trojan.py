#!/usr/bin/env python
import requests
import subprocess
import os
import tempfile

def download(url):
    get_request = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write("this is a test")

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

download("") #file name
subprocess.Popen("", shell=True) #open file

download("") #file name
subprocess.call("", shell=True) #open file

os.remove("")#file1
os.remove("")#file2