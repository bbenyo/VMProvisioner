#!/bin/bash
set -x

mkdir -p /opt/provisioners/scapy
rm /opt/provisioners/scapy/provision.sh

# Provision scapy
# Unzip master.zip
mkdir -p /opt/scapy
mv /tmp/master.zip /opt/scapy
cd /opt/scapy
unzip -of master.zip

cd scapy-master
sudo python3 setup.py install

pip3 install mathplotlib
pip3 install pyx
pip3 install cryptography
pip3 install sphinx
pip3 install sphinx_rtd_theme
pip3 install tox

cd doc/scapy
make html

# Save this provisioner script

# Bookkeeping
date > /opt/provisioner-date
echo "scapy" >> /opt/provisioner-packages
cp /tmp/provision.sh /opt/provisioners/scapy


