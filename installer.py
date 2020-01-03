#!/usr/bin/python3

import os
import subprocess
import tarfile
import argparse
import configparser
import paramiko
import time
import shutil

from glob import glob

indent=""
sshclient=None

def getPackages():
    plist = glob('*/')
    todoList = []
    for p in plist:
        pname = p[:-1]
        if not pname in installedPackages:
            todoList.append(pname)
    return todoList

def installPackage(name):
	global indent
	print("  Installing "+name)

	# 1: Copy over all tarballs
	tarList = glob(name+"/*.tar.gz")
	for t in tarList:
		print("    TarFile: "+t)
		indent="    "
		scpFile(t, "/tmp/"+os.path.basename(t))

	# 2: Copy over all files in files subdir
	filesSubdir = os.path.join(name, "files")
	if os.path.exists(filesSubdir):
		print("    Copying over files subdirectory")
		with tarfile.open(name+"/files.tar.gz", "w:gz") as filesTar:
			fList = glob(filesSubdir+"/**", recursive=True)
			for fname in fList:
				print("      adding: "+fname)
				filesTar.add(fname)
			filesTar.close()
			scpFile(os.path.join(name, "files.tar.gz"), "/tmp/"+name+"-files.tar.gz")
			os.remove(os.path.join(name, "files.tar.gz"))

	# 3: Copy over provision.sh if it exists
	provision = os.path.join(name, "provision.sh")
	if os.path.exists(provision):
		print("    Copying over provision.sh")
		scpFile(provision, "/tmp/provision.sh")
		print("    Executing provision.sh")
		sshCommandExec("chmod 774 /tmp/provision.sh; /tmp/provision.sh")
					
	installedPackages.append(name)

def handleWorkList(worklist):
	installedOne = False
	for pname in worklist:
		print("Handling "+pname)

		if pname in installedPackages:
			print(pname+" already installed, this shouldn't happen")
			continue
	
		# Get dependencies
		deps = os.path.join(pname, "dependency.txt")
		print("  Looking for "+deps)
		
		if os.path.exists(deps):
			print("  Dependency.txt found for "+pname)
			with open(deps) as depsFile:
				dependencyList = depsFile.readlines()
				print("  Dependency List: "+str(dependencyList))
				allIn = True
				for dep in dependencyList:
					depName = dep.strip()
					if depName in installedPackages:
						print("    "+depName+" installed")
					else:
						print("    "+depName+" not yet installed")
						allIn = False
					
				if allIn:
					installPackage(pname)
					installedOne = True
					
		else:
			print("  No dependency.txt found for "+pname)
			installPackage(pname)
							
	return installedOne

def localCommand(command):
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out,err = proc.communicate() # TODO: Timeout?
	ret = out.decode('utf-8')
	print("Stderr: "+err.decode('utf-8'))
	return ret
		
def sshCommandExec(command):
	if targetLocal:
		return localCommand(command)

	else:
		if sshclient == None:
			print("no sshclient, exiting")
			exit(1)
		
		stdin, stdout, stderr = sshclient.exec_command(command)
		print(indent+"Receiving command results for "+command)

		err=stderr.read()
		while len(err) > 0:
			print(err.decode("utf-8"))
			err=stderr.read()
	
		foo=stdout.read()
		ret = None
		while len(foo) > 0:
			ret = foo.decode("utf-8")
			print(ret)
			foo = stdout.read()
		
		return ret

def scpFile(localfile, remotefile):

	if targetLocal:
		remotefile = targetRoot+remotefile
		shutil.copyfile(localfile, remotefile)
	else:
		print(indent+"scp "+localfile+" "+remotefile)
		if sshclient == None:
			print("no sshclient, exiting")
			exit(1)
			
		scpClient = sshclient.open_sftp()
		scpClient.put(localfile, remotefile)
		scpClient.close()
	
###################################################
# Main
###################################################

parser = argparse.ArgumentParser()
parser.add_argument("-t", default="target.env", help="Target environment file")
args = parser.parse_args()
targetEnv = args.t

config = configparser.RawConfigParser({'target.local':'false'})
config.read(targetEnv)

targetLocal=config.getboolean('Target','target.local')
if targetLocal == True:
	print("Using local target")
	targetRoot=config.get('Target','target.root')
	print("Provisioning to targetRoot: "+targetRoot)
else:
	print("Using remote target")

	targetHost=config.get('Target', 'target.ssh.host')
	targetPort=config.get('Target', 'target.ssh.port')
	targetUser=config.get('Target', 'target.user')
	targetHostname=config.get('Target', 'target.hostname')
	keyFile=config.get('Target', 'target.ssh.keyFile')

	print("Accessing target at "+targetHost+":"+targetPort+" as "+targetUser+" with "+keyFile)

	sshclient = paramiko.SSHClient();
	sshclient.load_system_host_keys()
	sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	sshclient.load_system_host_keys()

	print ("Attempting to connect...")
	sshclient.connect(targetHost, targetPort, key_filename=keyFile, username=targetUser)
	sshret = sshCommandExec("hostname")

	if sshret.strip() == targetHostname:
		print("SSH successful")
	else:
		print("Returned '"+sshret+"'")
		print("SSH command failed")
		sshclient.close()
		exit(1)	

	
installedPackages = []
installPackage("base")
worklist = getPackages()

while (len(worklist) > 0):
	print("Handling worklist: "+str(len(worklist))+" packages left")
	installedOne = handleWorkList(worklist)
	if not installedOne:
		print("No progress made.  Remaining uninstalled packages: "+str(worklist))
		break
	else:
		worklist = getPackages()

print("Installer completed")
print("Installed: "+str(installedPackages))
	
if sshclient != None:
	sshclient.close()
