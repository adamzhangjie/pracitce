# insert_data.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
 
# import MySQLdb
 
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306, db='cmdb')
    cur=conn.cursor()
     
    # conn.select_db('cmdb')
 
 	sql_co = """INSERT into cmdb_server(cmdb_server_id, cmdb_server_hardwareid, cmdb_server_sequence, cmdb_server_arch_type, cmdb_server_vm_type, cmdb_server_vm_type, cmdb_server_machine_type,cmdb_server_machine_modelcmdb_server_cpuinfo,cmdb_server_memoryinfo,cmdb_server_diskinfo)
 	VALUES ('1', '2', '3', '4','5','6','7','8','9','10')"""
    
    cur.execute(sql_co)
    # conn.commit()
    # count=cur.execute('select * from cmdb_server')
    # print 'there has %s rows record' % count
 
    # result=cur.fetchone()
    # print result
    # print 'ID: %s info %s' % result
 
    # results=cur.fetchmany(5)
    # for r in results:
    #     print r
 
    # print '=='*10
    # cur.scroll(0,mode='absolute')
 
    # results=cur.fetchall()
    # for r in results:
    #     print r[1]
     
 
    conn.commit()
    cur.close()
    conn.close()
 
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])