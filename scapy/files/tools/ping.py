#!/usr/bin/python3

import sys
from scapy.all import IP,ICMP,L3RawSocket,conf,srloop

conf.L3socket=L3RawSocket

if len(sys.argv) < 2:
    print("Usage: ping host count")
    exit

pinger = IP(dst=sys.argv[1])/ICMP()
resp = srloop(pinger, count=int(sys.argv[2]))
if resp:
    print("Ping response: "+str(resp))
    for p in range(0,len(resp[0])):
        resp[0][p][1].show()
else:
    print("No answer")

