#!/bin/bash
set -x
# Provision base

# Install default packages
date > /opt/provisioner-date
echo "base" >> /opt/provisioner-packages

sudo apt-get -y install openjdk-8-jdk-headless
sudo apt-get -y install python3
sudo apt-get -y install python

mkdir /opt/base
cd /opt
mv /tmp/base-files.tar.gz /opt
tar xzvf base-files.tar.gz 

mv /tmp/test.tar.gz /opt/base
cd /opt/base
tar xzvf /opt/base/test.tar.gz

ls -ltr /opt/base
