#!/usr/bin/python3

import sys
from scapy.all import sniff, ARP

whosHere = {}

def arp_display(pkt):
    if pkt[ARP].op == 1: # who-has
        return f"Request {pkt[ARP].psrc} is asking about {pkt[ARP].pdst}"
    if pkt[ARP].op == 2:
        whosHere[str(pkt[ARP].hwsrc)] = pkt[ARP].psrc
        return f"*Response: {pkt[ARP].hwsrc} has address {pkt[ARP].psrc}"
    return "Unknown op: {pkt[ARP].op}"

packets = sniff(prn=arp_display, filter="arp", store=0, count=100)

print(packets.summary())
print(str(whosHere))
