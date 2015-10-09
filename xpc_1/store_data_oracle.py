#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cx_Oracle as oc

#方法主要用于将获取的静态或动态信息存储至数据库中，如果数据库中已存在，那么更新存在的信息
class StoreData(object):
	#数据库对象初始化，初始化内容为数据库连接
	def __init__(self, conn):
		self.conn = conn

	#检查服务器信息是否已存在数据库中，存在返回True，否则返回False
	def check_server_available(self, server_sequence):
		try:
			cursor = self.conn.cursor() #新建游标
			sql = "select * from CMDB_REGISTER_SERVER\
			 where CRS_SEQUENCE = '%s' " % server_sequence
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
			sql_insert = "INSERT into CMDB_REGISTER_SERVER\
			(CRS_SEQUENCE, \
				CRS_CONSTRUCT, \
				CRS_VM_TYPE, \
				CRS_TYPE, \
				CRS_MODEL,\
				CRS_CPUINFO, \
				CRS_MEMORYINFO,\
				CRS_DISKINFO,\
				CRS_IPADRESS, \
				CRS_OSNAME, \
        		CRS_STATE) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s', '%s', '%s', '%s')" % ( server_sequence, server_dict_data['server_arch_type'], server_dict_data['server_vm_type'], server_dict_data['server_machine_type'], server_dict_data['server_machine_model'], server_dict_data['server_cpuinfo'], server_dict_data['server_memoryinfo'], server_dict_data['server_diskinfo'], server_dict_data['server_manageIP'], server_dict_data['server_os_info'],'0')
			# print sql_insert
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
			sql_update = "UPDATE CMDB_REGISTER_SERVER \
			set CRS_CONSTRUCT = '%s' , \
			CRS_VM_TYPE = '%s' , \
			CRS_TYPE = '%s' , \
			CRS_MODEL = '%s' , \
			CRS_CPUINFO = '%s' , \
			CRS_MEMORYINFO = '%s' , \
			CRS_DISKINFO = '%s', \
			CRS_IPADRESS = '%s', \
			CRS_OSNAME = '%s'  \
			WHERE CRS_SEQUENCE = '%s' " %(server_dict_data['server_arch_type'], server_dict_data['server_vm_type'], server_dict_data['server_machine_type'], server_dict_data['server_machine_model'], server_dict_data['server_cpuinfo'], server_dict_data['server_memoryinfo'], server_dict_data['server_diskinfo'],server_dict_data['server_manageIP'], server_dict_data['server_os_info'], server_sequence)
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
			if self.check_server_available(server_sequence):
				print 'Begin to update  a server(%s) infomation!' %(server_sequence)
				self.update_a_server(server_sequence, server_dict_data)
			else:
				print 'Begin to insert  a new server(%s) infomation!' %(server_sequence)
				self.insert_a_newserver(server_sequence,server_dict_data)
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
	conn = oc.Connection('jpre/jpre@NBCB_8.99.1.68')
	st_data = StoreData(conn)
	server_dict_data = {"server_memoryinfo": "3", "server_arch_type": "x86", "server_sequence": "VMware-42 22 4e e7 fc ea 4a 19-ec 34 42 11 24 da e4 f9", "server_manageIP": "127.0.0.1", "server_vm_type": "x86-vm", "server_machine_model": "", "server_os_info": "Oracle Linux Server release 6.3", "server_cpuinfo": 2, "server_machine_type": "", "server_diskinfo": "117G"}
	try:
		st_data.send_staticInfo(server_dict_data["server_sequence"], server_dict_data)
	except Exception as e:
		print "出现问题：",e
	finally:
		conn.close()





