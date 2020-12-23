#!/bin/bash
set -x

# Remove any existing provisioner script from opt
mkdir -p /opt/provisioners/cloud
rm /opt/provisioners/cloud/provision.sh

# Provision cloud
# bucket_filder
mkdir -p /opt/cloud
mv /tmp/bucket_finder_1.1.tar.gz /opt/cloud
cd /opt/cloud
tar xzvf bucket_finder_1.1.tar.gz
echo grumpy > wordlist.txt

# Save this provisioner script
# Bookkeeping
date > /opt/provisioner-date
echo "cloud" >> /opt/provisioner-packages
cp /tmp/provision.sh /opt/provisioners/cloud


