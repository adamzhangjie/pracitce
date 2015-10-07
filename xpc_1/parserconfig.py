# parserconfig.py
# !/usr/env/bin python
# -*- encoding:utf-8 -*-
import re


def parserSystemInfo():
	systeminfo = {}
	pat = r'(.*):(.*)'
	sys_re = re.compile(pat)
	with open('system1.txt','rt') as f:
		for line in f:
			m = sys_re.match(line)
			if m:
				systeminfo[m.group(1).strip()] = m.group(2).strip()

	return systeminfo
		
system_info = parserSystemInfo().copy()
print system_info



conn=MySQLdb.connect(host='169.254.156.41',user='root',passwd='password',port=3306, db='cmdb')
