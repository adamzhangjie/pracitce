# agnet.py
# !/usr/bin/env python
# -*- encoding:utf-8 -*-
import os
import platform
import sys
from multiprocessing import cpu_count

# Check we're not using an old version of Python. Do this before anything else
# We need 2.7 above because some modules (like subprocess) were only introduced
# in 2.7. And checking the enviroment is staisfied requirement.

if int(sys.version_info[1]) <= 3:
	print """
	You are using an outdated version of Python. Please update to
    v2.7 """
    # sys.exit(1)

import subprocess
import socket

def getOSinfo_all():
	"""To obatin the System information
	this method used to get OS infromation 
	include all below items: 
	OS_tpye
	OS_version
	CPU_num
	RAM_volume
	
	"""
	agentPlatForm = platform.system()
	print agentPlatForm
	command_systeminfo = 'uname -a'
	command_HDD_linux = 'df -h'
	#get
	systeminfo = os.system(command_systeminfo)
	IPlist = socket.gethostbyname(socket.gethostname())
	HDD_linux = os.popen(command_HDD_linux)
	isx86_type = True
	isvware_tpye = True
	machine_tpye = '' #machine tpye include IBM_P IBM_I HUAWEI_X
	machine_model = '' # machine version IBM P710 e.t.
	machine_serialNum = ''
	# p = subprocess.Popen(command,
	# 					stdin = subprocess.PIPE,
	# 					stdout = subprocess.PIPE,
	# 					stderr = subprocess.STDOUT,
	# 					shell = False,
	# 					close_fds = sys.platform.startswith('win'),
	# 					universal_newlines = True,
	# 					env = os.environ)
	return systeminfo, HDD_linux, IPlist

def getDiskSpace(systemTpye):
	'''get the Disk Space information
	include below items:
	1-totalSpace
	2-usedSpace
	3-usedPencentage
	return a list zip all the information
	'''
	if systemTpye == 'Linux':
		p = os.popen('df -h /')
		p.readline()
		SpaceInfo = p.readline()
		return SpaceInfo.split()[1:5]

def getRaminfo(systemType):
	'''get the Ram information
	include below items:
	1-totalRam:
	2-usedRam:
	3-freeRam:
	return a list zip all the information
	'''
	#Linux type
	if systemType == 'Linux':
		p = os.popen('free')
		p.readline()
		RamInfo = p.readline()
		return RamInfo.split()[1:4] 

def getCPUinfo(systemType):
	'''get the CPU information
	include below items:
	1-CPUNum:
	2-
	'''
	#Linux type
	if systemType == 'Linux':
		CPUNum = cpu_count()
		p = os.popen('lscpu')
		cpu_arch = p.readline().splie()[1:1]
		return CPUNum,cpu_arch

def isx86Arch(systemType):
	if systemType == 'Linux':
		p = os.popen('lscpu')
		cpu_arch = p.readline().splie()[1:2]
		if cpu_arch[0].startswith('x86'):
			return True
		else:
			return False

def isVM(systemType):
	if systemType == 'Linux':
		p = os.popen('dmidecode | grep VMware')
		if p is not None:
			return True
		else:
			return False
	pass

def getMachineType():
	if systemType == 'Linux':
		p = os.popen('d')

def getMachineModel():
	pass

def getMachineSerial(systemType):
	if systemType == 'Linux':
		p = os.popen('dmidecode | grep UUID')
		if p is not None:
			return True
		else:
			return False
	pass

def getIpList():
	pass

print getOSinfo_all()
print getDiskSpace('Linux')
print getRaminfo('Linux')
print getCPUinfo('Linux')
print getMachineSerial('Linux')
