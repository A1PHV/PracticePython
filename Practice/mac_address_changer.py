#!/usr/bin/env python
import subprocess
import optparse
import re

def get_argument():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Use --help")
    elif not options.new_mac:
        parser.error("[-] Use --help for more info")
    return options

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_result = ifconfig_result.decode("utf-8")
    print(ifconfig_result)

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-]Coudn't read MAC")

def change_mac(interface, new_mac):
    print("Change for " + interface + " to " + new_mac)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

options = get_argument()

current_mac = get_current_mac(options.interface)
print("Current mac: " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
print("[+] MAC was successfully changed")


