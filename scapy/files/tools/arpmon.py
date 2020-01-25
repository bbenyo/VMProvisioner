#!/usr/bin/python3

import sys
from scapy.all import sniff

whosHere = []

def arp_display(pkt):
    if pkt[ARP].op == 1: # who-has
        return f"Request {pkt[ARP].psrc} is asking about {pkt[ARP].pdst}"
    elif pkt[ARP].op == 2:
        whosHere[pkt[ARP].hwsrc] = pkt[ARP].psrc
        return f"*Response: {pkt[ARP].hwsrc} has address {pkt[ARP].psrc}"

packets = sniff(count=10)
print(packets.summary())

print(str(whosHere))
