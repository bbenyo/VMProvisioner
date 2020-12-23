#!/usr/bin/python3

import sys
import json
import os.path
from datetime import datetime
from scapy.all import sniff, ARP, AsyncSniffer
import threading

dsLock = threading.Lock()

class Host(object):
    mac = None
    ipv4 = None
    lastSeen = None
    name = None

    # Historical MACs for this IP
    previousMacs = []
    # Historical IPs for this MAC
    previousIPs = []

    def __init__(self, mac, ip, name=None, lastSeen=None, previousMacs=[], previousIPs=[]):
        self.mac = mac
        self.ipv4 = ip
        if name is None:
            self.name = mac
        else:
            self.name = name

        if lastSeen is None:
            self.lastSeen = datetime.now().timestamp()
        else:
            self.lastSeen = lastSeen

        self.previousMacs = previousMacs
        self.previousIPs = previousIPs

    def seen(self):
        self.lastSeen = datetime.now().timestamp()

    def newIP(self, ip1):
        if ip1 not in self.previousIPs:
            self.previousIPs.append(ip1)
        self.ipv4 = ip1

    def newMAC(self, mac1):
        if mac1 not in self.previousMacs:
            self.previousMacs.append(mac1)
        self.mac = mac1

    def __str__(self):
        return "Host %s: ipv4: %s mac: %s lastSeen: %s pMacCount: %d pIPCount: %d" % (self.name, self.ipv4, self.mac, self.lastSeen, len(self.previousMacs), len(self.previousIPs))


class HostEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Host):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def decodeHost(dct):
    if 'previousIPs' in dct:
        h1 = Host(dct['mac'], dct['ipv4'], dct['name'], dct['lastSeen'], dct['previousIPs'], dct['previousMacs'])
        return h1
    return dct


hostByMac = {}
hostByIP = {}
whosHere = {}

if os.path.exists('whoshere.json'):
    with open('whoshere.json', 'r') as f:
        whosHere = json.load(f)
        print("Loaded from whoshere.json")
        print(str(whosHere))

if os.path.exists('hosts.json'):
    with open('hosts.json', 'r') as f:
        hostList = json.load(f, object_hook=decodeHost)
        print("Loaded from hosts.json")
        count = 0
        for h in hostList:
            host = hostList.get(h)
            hostByMac[h] = host
            hostByIP[host.ipv4] = host
            count = count + 1
            print(host)

        print("Loaded " + str(count) + " hosts")

verbose = True


def arp_display(pkt):
    mac1 = pkt[ARP].hwsrc
    ip1 = pkt[ARP].psrc
    whosHere[mac1] = ip1

    h = hostByMac.get(mac1, None)
    if h is not None:
        h.seen()
        if not h.ipv4 == ip1:
            print("Warn: Host " + str(h.name) + " has a new IP: " + str(h.ipv4) + " -> " + str(ip1))
            h.newIP(ip1)
        else:
            if verbose:
                print("Known host: " + str(h.name))
    else:
        dsLock.acquire()
        h = Host(mac1, ip1)
        hostByMac[mac1] = h
        dsLock.release()

    h2 = hostByIP.get(ip1, None)
    if h2 is not None:
        if not h2.mac == mac1:
            if verbose:
                print("IP " + str(ip1) + " has a new MAC: " + str(mac1))
            h2.newMAC(mac1)
            if len(h2.previousMacs) > 1:
                print("Warn: IP " + str(ip1) + " has had " + str(len(h2.previousMacs)) + " previous mac addresses")
    else:
        dsLock.acquire()
        hostByIP[ip1] = h
        h2 = h
        dsLock.release()

    if pkt[ARP].op == 1:  # who-has
        if pkt[ARP].psrc == pkt[ARP].pdst:
            if verbose:
                return f"Announcement for {pkt[ARP].psrc} mac {pkt[ARP].hwsrc}"
            else:
                return None
        else:
            if verbose:
                return f"Request {pkt[ARP].psrc} is asking about {pkt[ARP].pdst}"
            else:
                return None

    if pkt[ARP].op == 2:
        whosHere[str(pkt[ARP].hwsrc)] = pkt[ARP].psrc
        if verbose:
            return f"*Response: {pkt[ARP].hwsrc} has address {pkt[ARP].psrc}"
        else:
            return None

    if verbose:
        return "Unknown op: {pkt[ARP].op}"
    else:
        return None


print("ARP Sniffing...")
snf = AsyncSniffer(prn=arp_display, filter="arp", store=0)
snf.start()
# time.sleep(10)


def sniff_stop():
    packets = snf.stop()

    print(packets.summary())
    print(str(whosHere))
    output()


def output():
    with open('whoshere.json', 'w') as f:
        json.dump(whosHere, f)
        print("Wrote to whoshere.json")

    dsLock.acquire()
    with open('hosts.json', 'w') as f:
        json.dump(hostByMac, f, cls=HostEncoder)
        print("Wrote to hosts.json")
    dsLock.release()


stop = False
while not stop:
    cmd = input("> ")
    if cmd == 'stop' or cmd == 's':
        print("Stopping")
        sniff_stop()
        stop = True
    elif cmd == 'v' or cmd == 'verbose':
        print("Verbose ON")
        verbose = True
    elif cmd == 'q' or cmd == 'quiet':
        print("Verbose OFF")
        verbose = False
    elif cmd == 'o' or cmd == 'output':
        print("Writing output files")
        output()
    elif cmd == 'l' or cmd == 'list':
        dsLock.acquire()
        for h in hostByMac:
            h1 = hostByMac[h]
            print(h1)
        dsLock.release()
