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
	'server_diskinfo':'',
	'server_manageIP':''} #获取机器硬盘信息


	# def getOSinfo_all():
	# 	"""To obatin the System information
	# 	this method used to get OS infromation 
	# 	include all below items: 
	# 	OS_type
	# 	OS_version
	# 	CPU_num
	# 	RAM_volume
		
	# 	"""
	# 	agentPlatForm = platform.system()
	# 	return agentPlatForm
	# 	# print agentPlatForm
	# 	# command_systeminfo = 'uname -a'
	# 	# command_HDD_linux = 'df -h'
	# 	# #get
	# 	# systeminfo = os.system(command_systeminfo)
	# 	# IPlist = socket.gethostbyname(socket.gethostname())
	# 	# # HDD_linux = os.popen(command_HDD_linux)
	# 	# isx86_type = True
	# 	# isvware_type = True
	# 	# machine_type = '' #machine type include IBM_P IBM_I HUAWEI_X
	# 	# machine_model = '' # machine version IBM P710 e.t.
	# 	# machine_serialNum = ''
	# 	# # p = subprocess.Popen(command,
	# 	# # 					stdin = subprocess.PIPE,
	# 	# # 					stdout = subprocess.PIPE,
	# 	# # 					stderr = subprocess.STDOUT,
	# 	# # 					shell = False,
	# 	# # 					close_fds = sys.platform.startswith('win'),
	# 	# # 					universal_newlines = True,
	# 	# # 					env = os.environ)
	# 	# return systeminfo, HDD_linux, IPlist


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
		p = os.popen('free -g')
		p.readline()
		p.readline()
		RamInfo = p.readline()
		return RamInfo.split()[1:4] 

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
		return CPUNum,cpu_arch

	# def isx86Arch(systemType):
	# 	if systemType == 'Linux':
	# 		p = os.popen('lscpu')
	# 		cpu_arch = p.readline().splie()[1:2]
	# 		if cpu_arch[0].startswith('x86'):
	# 			return True
	# 		else:
	# 			return False

	# def isVM(systemType):
	# 	if systemType == 'Linux':
	# 		p = os.popen('dmidecode -t 1 | grep VMware')
	# 		if p is not None:
	# 			# p.close()
	# 			return True
	# 		else:
	# 			return False
	# IBM-P,IBM-I,HUAWEI-X类别
	# def getMachineType():
	# 	if systemType == 'Linux':
	# 		p = os.popen('dmidecode -t 1 | grep Manufacturer')
	# # 设备型号
	# def getMachineModel():
	# 	pass

	# def getMachineSerial(systemType):
	# 	if systemType == 'Linux':
	# 		p = os.popen('dmidecode -t 1 | grep UUID')
	# 		if p is not None:
	# 			return p.readline().split()[1:][0]
	# 		else:
	# 			return False
	# 	# pass

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
		return p.readline().split()[:2]

	#获取组织好的系统信息内容
	def getOrganizedInfo(self):
		self.server_static_dict_data['server_sequence'] = self.parserSystemInfo()[0] #获取序列号信息
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


if __name__ == '__main__':
	
	# print getOSinfo_all()
	# print 'DiskSpace is:', getDiskSpace('Linux')
	# print 'Ram is :', getRaminfo('Linux')[0]
	# print 'cpu_arch is:', getCPUinfo('Linux')[1]
	# print 'cpu_core_num is:',getCPUinfo('Linux')[0]
	# print 'UUID is :', getMachineSerial('Linux')
	# print 'isVM :', isVM('Linux')
	# print 'os versino info:',getOSinfo('Linux')
	# system_info = parserSystemInfo().copy()
	# print system_info
	# print 'IP is:', getIpList()
	# # print isVM('Linux')

	server_info = ServerInfo_linux()
	server_info.getOrganizedInfo()
	print server_info.server_static_dict_data
