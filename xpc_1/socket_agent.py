# socket_agent.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script should implement a agent in a server 
# send back server information to socket_server
# It can also implement 

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.connect(('localhost', 9999))

	print s.recv(1024).decode('utf-8')
	# s.send(b'exit')
	# print s.recv(1024).decode('utf-8')

	for data in [b'Michael', b'Tracy', b'Sarah', b'Adma', b'Good', b'Find']:
		s.send(data)
		print s.recv(1024).decode('utf-8')
	# print s.recv(1024).decode('utf-8')
	s.send(b'exit')
except Exception, e:
	print e
finally:
	s.close()