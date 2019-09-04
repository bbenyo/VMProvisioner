# VMProvisioner
Provisioner to load tools and set up a virtual machine from a base image, simpler than Ansible/Salt/Puppet/etc.

Useful for when you're adding many individual components and don't want to create ansible playbooks or salt pillars/modules for each

# Each subdirectory can contain an upload.sh script, a provision.sh script, and a dependency.txt file

## name.tar.gz
tarball to scp over to /tmp.  Provision.sh should install it

## files subdirectory
tar'd and scp'd over to /tmp/name-files.tar.gz

## provision.sh
This script is run through ssh on the target VM after any tarball has been uploaded.  It should set up the local environment as necessary

## dependency.txt
This is a text file of project names, one on a line.  Project names correspond to the subdirectories from this root directory, that contain thet files and upload/provision scripts.  These dependencies are used by the main installer to order the subdirectories, a given project will be provisioned only after all dependencies have been provisioned.
