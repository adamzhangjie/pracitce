#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

# 打开数据库连接
conn=MySQLdb.connect(host='192.168.199.130',user='root',passwd='password',port=3306, db='cmdb')

# 使用cursor()方法获取操作游标 
cursor = conn.cursor()

# SQL 插入语句
hardware_id = '2'

sql_query = "select * from cmdb_server where cmdb_server_hardwareid = "+"'"+hardware_id+"'"

sql_insert = """INSERT into cmdb_server(
	cmdb_server_id, 
	cmdb_server_hardwareid, 
	cmdb_server_sequence, 
	cmdb_server_arch_type, 
	cmdb_server_vm_type, 
	cmdb_server_machine_type,
	cmdb_server_machine_model, 
	cmdb_server_cpuinfo,
	cmdb_server_memoryinfo,
	cmdb_server_diskinfo)
 	VALUES (
 		'1', 
 		'2', 
 		'3', 
 		'4',
 		'5',
 		'6',
 		'7',
 		'8',
 		'9',
 		'10')"""
    
try:
   # 执行sql语句
   cursor.execute(sql_query)
   count = cursor.count
   if count == 0:
   	cursor.execute(sql_insert)
   else:
   	pass
   # 提交到数据库执行
   conn.commit()
except Exception, e:
   # Rollback in case there is any error
   print e
   conn.rollback()

# 关闭数据库连接
conn.close()