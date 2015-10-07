# socketserver_sample.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from SocketServer import TCPServer, StreamRequestHandler, ForkingMixIn, ThreadingMixIn

class Server(ThreadingMixIn, TCPServer):
	pass

class Handler(StreamRequestHandler):

	def handle(self):
		addr = self.request.getpeername()
		print 'Got connection from', addr
		self.data = self.request.recv(1024).strip()
		message_data = json.loads(self.data)
		print message_data
		print message_data['SKU Number']
		self.wfile.write('thank you for connection')

server = Server(('', 1234), Handler)
print '-----------------  Beging to server !  -------------------'

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()