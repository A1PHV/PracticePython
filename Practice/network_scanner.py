#!/usr/bin/env python
import scapy.all as scapy
import optparse

def get_arg():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP")
    (options, arguments) = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    client_list = []
    for el in answered_list:
        client_dict = {"ip": el[1].psrc, "mac": el[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for client in results_list:
        print(client["ip"] + '\t\t' + client["mac"])

options = get_arg()

scan_result = scan(options.target)

print_result(scan_result)





