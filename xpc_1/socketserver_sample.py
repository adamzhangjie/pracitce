#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from SocketServer import TCPServer, StreamRequestHandler, ForkingMixIn, ThreadingMixIn
from store_data_oracle import StoreData
import cx_Oracle as oc

class Server(ThreadingMixIn, TCPServer):
	pass

class Handler(StreamRequestHandler):

	def handle(self):
		addr = self.request.getpeername()
		print ''
		print ''
		print '------------------Got connection from-------------------', addr
		self.data = self.request.recv(1024).strip()
		message_data = json.loads(self.data)
		conn = oc.Connection('jpre/jpre@NBCB_8.99.1.68')
		try:
			st_data = StoreData(conn)
			server_dict_data=message_data.copy()
			server_sequence = server_dict_data['server_sequence']
			st_data.send_staticInfo(server_sequence, server_dict_data)
		except Exception as e:
			print "数据库操作出现问题：",e
		finally:
			conn.close()
		print message_data
		self.wfile.write('thank you for connection')

server = Server(('', 1234), Handler)
print '-----------------  Beging to server !  -------------------'

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()