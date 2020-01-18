#!/usr/bin/python3

import sys
from scapy.all import sr1,IP,ICMP,L3RawSocket,conf

conf.L3socket=L3RawSocket

p = sr1(IP(dst=sys.argv[1])/ICMP())
if p:
    p.show()
else:
    print("Nothing")

