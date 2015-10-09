# -*- coding: utf-8 -*-


import os
import platform
import sys
import re
from multiprocessing import cpu_count

# Check we're not using an old version of Python. Do this before anything else
# We need 2.7 above because some modules (like subprocess) were only introduced
# in 2.7. And checking the enviroment is staisfied requirement.

if int(sys.version_info[1]) <= 3:
	print """
	You are using an outdated version of Python. Please update to
    v2.7 """
    # sys.exit(1)
# import subprocess
import socket

#服务器信息类
class ServerInfo_linux(object):
	def __init__(self):
		self.server_static_dict_data = {
	'server_sequence':'', 
	'server_arch_type':'', 
	'server_vm_type':'', 
	'server_machine_type':'', #机器类型 IBM_P, IBM_I,HUAWEI_X
	'server_machine_model':'', #机器型号 520
	'server_cpuinfo':'',
	'server_memoryinfo':'',
	'server_diskinfo':'', #获取机器硬盘信息
	'server_manageIP':'',
	'server_os_info':''} 



	#获取磁盘空间信息
	def getDiskSpace(self):
		'''get the Disk Space information
		include below items:
		1-totalSpace
		2-usedSpace
		3-usedPencentage
		return a list zip all the information
		'''
		p = os.popen('df -h /')
		p.readline()
		p.readline()
		SpaceInfo = p.readline()
		return SpaceInfo.split()[1:5]

	#获取内存基本信息
	def getRaminfo(self):
		'''get the Ram information
		include below items:
		1-totalRam:
		2-usedRam:
		3-freeRam:
		return a list zip all the information
		'''
		#Linux type 不同linux 不同的方法
		p = os.popen('free -g ')
		p.readline()
		RamInfo = p.readline()
		RamSize = RamInfo.split()[1:2]
		return  RamSize 

	#获取CPU基本信息
	def getCPUinfo(self):
		'''get the CPU information
		include below items:
		1-CPUNum:
		2-
		'''
		#Linux type
		CPUNum = cpu_count()
		p = os.popen('lscpu')
		cpu_arch = p.readline().split()[1:][0]
		t = os.popen('cat /proc/cpuinfo | grep name |cut -f2 -d: |uniq -c')
		CPUinfo = t.readline().strip()
		return CPUinfo,cpu_arch

	#获取解释后的系统信息
	def parserSystemInfo(self):
		systeminfo = {}
		pat = r'(.*):(.*)'
		sys_re = re.compile(pat)
		# with open('system1.txt','rt') as f:
		p = os.popen(r'dmidecode -t 1')
		for line in p:
			m = sys_re.match(line)
			if m:
				systeminfo[m.group(1).strip()] = m.group(2).strip()
		return systeminfo['Serial Number'], systeminfo['Manufacturer'], systeminfo['Product Name']

	#获取IP地址信息
	def getManageIP(self):
		IP = socket.gethostbyname(socket.gethostname())
		return IP
	#获取操作信息
	def getOSinfo(self):
		p = os.popen('cat /etc/issue')
		return p.readline().strip()

	#获取组织好的系统信息内容
	def getOrganizedInfo(self):
		self.server_static_dict_data['server_sequence'] = self.parserSystemInfo()[0].replace(' ', '') #获取序列号信息
		if self.getCPUinfo()[1][:3].startswith('x86'): #获取架构信息
			self.server_static_dict_data['server_arch_type'] = 'x86'
		else:
			self.server_static_dict_data['server_arch_type'] = 'not x86'
		if not self.server_static_dict_data['server_sequence'].startswith('VMware'):
			self.server_static_dict_data['server_vm_type'] = 'not vm'
		elif self.server_static_dict_data['server_sequence'].startswith('VMware') and self.server_static_dict_data['server_arch_type'] == 'x86':
			 self.server_static_dict_data['server_vm_type'] = 'x86-vm'
		else:
			self.server_static_dict_data['server_vm_type'] = 'not x86-vm'
		if self.server_static_dict_data['server_vm_type'] == 'not vm':
			if self.parserSystemInfo()[1].strip() == "IBM":
				self.server_static_dict_data['server_machine_type'] = "IBM_I"
				self.server_static_dict_data['server_machine_model'] = self.parserSystemInfo()[2]
			else:
				self.server_static_dict_data['server_machine_type'] = "HUAWEI_X"
				self.server_static_dict_data['server_machine_model'] = self.parserSystemInfo()[2]
		self.server_static_dict_data['server_memoryinfo'] = self.getRaminfo()[0] #获取内存信息
		self.server_static_dict_data['server_cpuinfo'] = self.getCPUinfo()[0] #获取cpu信息
		self.server_static_dict_data['server_diskinfo'] = self.getDiskSpace()[0] #获取硬盘空间信息
		self.server_static_dict_data['server_manageIP'] = self.getManageIP() #获取IP地址信息
		self.server_static_dict_data['server_os_info'] = self.getOSinfo() #获取操作系统信息


if __name__ == '__main__':
	
	server_info = ServerInfo_linux()
	server_info.getOrganizedInfo()
	print server_info.server_static_dict_data
