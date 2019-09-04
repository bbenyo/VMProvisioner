#!/bin/bash
set -x
# Provision base

# Install default packages
date > /opt/provisioner-date
echo "base" >> /opt/provisioner-packages

sudo apt-get -y install openjdk-8-jdk-headless
sudo apt-get -y install python3
sudo apt-get -y install python

