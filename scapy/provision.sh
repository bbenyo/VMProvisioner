#!/bin/bash
set -x

mkdir -p /opt/provisioners/scapy
rm /opt/provisioners/scapy/provision.sh

# Provision scapy
# Unzip master.zip
mkdir -p /opt/scapy
mv /tmp/master.zip /opt/scapy
cd /opt/scapy
unzip -o master.zip

cd scapy-master
sudo python3 setup.py install

python3 -m pip install ipython
python3 -m pip install matplotlib
python3 -m pip install pyx
python3 -m pip install cryptography
python3 -m pip install sphinx
python3 -m pip install sphinx_rtd_theme
python3 -m pip install tox

cd doc/scapy
make html

# Save this provisioner script

# Bookkeeping
date > /opt/provisioner-date
echo "scapy" >> /opt/provisioner-packages
cp /tmp/provision.sh /opt/provisioners/scapy


