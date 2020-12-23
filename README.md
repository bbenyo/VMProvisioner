# VMProvisioner
Provisioner to load tools and set up a virtual machine from a base image, simpler than Ansible/Salt/Puppet/etc.

Useful for when you're adding many individual components and don't want to create ansible playbooks or salt pillars/modules for each

## Subdirectories
Each subdirectory contains a single project.  Each project can contain tarballs, zips, extra files, and provisioner script
The installer will install each project if it doesn't already exist on the target host.  It checks for existance on the host by
an md5 checksum on the provisioner script.  Therefore, you can add a version comment to the provisioner to manage versions

Installation first ensures that all dependent projects are installed, by looking at any dependency.txt file.  The dependency.txt file
should contain a list of projects, one per line.

Installing a project involves
1. Copying over all tar.gz files in the project directory to /tmp
2. Copying over all .zip files to /tmp
3. Copying over the entire files subdirectory to /tmp as files.tar.gz, then expanding to /opt/[project name]
4. Copy over provision.sh to /tmp
5. Execute provision.sh on the target

Each subdirectory can contain tarballs, a files subdirectory, a provision.sh script, and a dependency.txt file

## *.tar.gz
tarball to scp over to /tmp.  Provision.sh should do whatever it needs to do with it

## *.zip
zips to scp over to /tmp, provision.sh should do whatever it needs to do with it

## files subdirectory
tar'd and scp'd over to /tmp/name-files.tar.gz

## provision.sh
This script is run through ssh on the target VM after any tarball has been uploaded.  It should set up the local environment as necessary

## dependency.txt
This is a text file of project names, one on a line.  Project names correspond to the subdirectories from this root directory, that contain thet files and upload/provision scripts.  These dependencies are used by the main installer to order the subdirectories, a given project will be provisioned only after all dependencies have been provisioned.
