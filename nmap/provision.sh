#!/bin/bash
set -x

# Bookkeeping
mkdir -p /opt/provisioners/nmap
rm /opt/provisioners/nmap/provision.sh

# Install default packages
ls -l
echo bar > /tmp/foo.txt
cat /tmp/foo.txt

sudo apt-get -y install nmap

# Install default packages
date > /opt/provisioner-date
echo "nmap" >> /opt/provisioner-packages
# Save this provisioner script
cp /tmp/provision.sh /opt/provisioners/nmap
