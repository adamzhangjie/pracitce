#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb

#方法主要用于将获取的静态或动态信息存储至数据库中，如果数据库中已存在，那么更新存在的信息
class StoreData(object):
	#数据库对象初始化，初始化内容为数据库连接
	def __init__(self, conn):
		self.conn = conn

	#检查服务器信息是否已存在数据库中，存在返回True，否则返回False
	def check_server_available(self, server_sequence):
		try:
			cursor = self.conn.cursor() #新建游标
			sql = "select * from cmdb_server\
			 where cmdb_server_hardwareid = '%s' " % server_sequence
			cursor.execute(sql)
			rs = cursor.fetchall()
			if len(rs) != 0:
				return True
			else:
				return False
		except Exception as e:
			print "检查服务器信息的时候报错 :",e
			raise e
		finally:
			cursor.close()

	#新增加一套服务器相关信息，包括序列号、架构类别、是否虚拟机、机器型号、CPU，内存、硬盘等
	def insert_a_newserver(self, server_sequence, server_dict_data):
		try:
			cursor = self.conn.cursor() #新建游标
			print "----Begin to insert the value-------"
			sql_insert = "INSERT into cmdb_server\
			(cmdb_server_sequence, \
				cmdb_server_arch_type, \
				cmdb_server_vm_type, \
				cmdb_server_machine_type, \
				cmdb_server_machine_model,\
				cmdb_server_cpuinfo, \
				cmdb_server_memoryinfo,\
				cmdb_server_diskinfo) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % ( server_sequence, '2','3','4','5','6','7','8','9')
			cursor.execute(sql_insert)
		except Exception as e:
			print "插入操作的过程中发生错误信息如：",e
			raise Exception("插入操作失败：")
		finally:
			cursor.close()


	#更新已有的一套服务器信息
	def update_a_server(self, server_sequence, server_dict_data):
		try:
			print "Beging to update the database info"
			cursor = self.conn.cursor() #新建游标
			sql_update = "UPDATE cmdb_server \
			set cmdb_server_arch_type = '%s' , \
			cmdb_server_vm_type = '%s' , \
			cmdb_server_machine_type = '%s' , \
			cmdb_server_machine_model = '%s' , \
			cmdb_server_cpuinfo = '%s' , \
			cmdb_server_memoryinfo = '%s' , \
			cmdb_server_diskinfo = '%s' \
			WHERE cmdb_server_hardwareid = '%s' " %('1', '2','3','4','5','6','y', server_sequence)
			# print sql_update
			cursor.execute(sql_update)
			rc = cursor.rowcount
		except Exception as e:
			print "更新操作过程出现错误 :" ,e
			# if len(rs) == 0:
			raise Exception("更新操作失败：")
		finally:
			cursor.close()


	#探测静态信息存储保存到数据库
	def send_staticInfo(self, server_sequence, server_dict_data):
		try:
			if self.check_server_available server_sequence):
				self.update_a_server server_sequence, server_dict_data)
			else:
				self.insert_a_newserver server_sequence,server_dict_data)
			self.conn.commit()
		except Exception as e:
			# print "Database error info:", e
			self.conn.rollback()
			raise e
	#定时探测动态信息存储到数据库
	def send_dynamicInfo(self, server_sequence, server_dict_data):
		pass



#单独的测试场景
if __name__ == '__main__':
	conn=MySQLdb.connect(host='169.254.156.41',user='root',passwd='password',port=3306, db='cmdb')
	st_data = StoreData(conn)
	server_dict_data={}
	try:
		st_data.send_staticInfo('002', server_dict_data)
	except Exception as e:
		print "出现问题：",e
	finally:
		conn.close()





