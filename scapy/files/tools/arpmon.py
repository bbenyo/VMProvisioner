#!/usr/bin/python3

import sys
import json
import os.path
from scapy.all import sniff, ARP, AsyncSniffer

whosHere = {}
if os.path.exists('whoshere.json'):
    with open('whoshere.json','r') as f:
        whosHere = json.load(f)
        print("Loaded from whoshere.json")
        print(str(whosHere))

def arp_display(pkt):
    if pkt[ARP].op == 1: # who-has
        return f"Request {pkt[ARP].psrc} is asking about {pkt[ARP].pdst}"
    if pkt[ARP].op == 2:
        whosHere[str(pkt[ARP].hwsrc)] = pkt[ARP].psrc
        return f"*Response: {pkt[ARP].hwsrc} has address {pkt[ARP].psrc}"
    return "Unknown op: {pkt[ARP].op}"

print("Sniffing...")
snf = AsyncSniffer(prn=arp_display, filter="arp", store=0)
snf.start()
time.sleep(300)
packets = snf.stop()

print(packets.summary())
print(str(whosHere))

with open('whoshere.json','w') as f:
    json.dump(whosHere, f)
    print("Wrote to whoshere.json")
