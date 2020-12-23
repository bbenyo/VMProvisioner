#!/bin/bash
set -x

# Bookkeeping
mkdir -p /opt/provisioners/base
rm /opt/provisioners/base/provision.sh

## Base provisioner
sudo apt-get -y install openjdk-8-jdk-headless
sudo apt-get -y install python3
sudo apt-get -y install python

sudo apt-get -y install python3-pip
sudo apt-get -y install python-pip

python3 -m pip install --upgrade pip
python -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools
python -m pip3 install --upgrade setuptools

sudo apt-get -y install ruby

mkdir /opt/base
mv /tmp/test.tar.gz /opt/base
cd /opt/base
tar xzvf /opt/base/test.tar.gz

ls -ltr /opt/base

# Install default packages
date > /opt/provisioner-date
# Base only overwrites provisioner-packages
echo "base" > /opt/provisioner-packages
# Save this provisioner script
cp /tmp/provision.sh /opt/provisioners/base
