# socket_server.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import threading
import time

def tcplink(sock, addr):
	print 'Accept new connection from %s :%s ..' %(addr)
	sock.send(b'Welcome!')
	while True:
		data = sock.recv(1024)
		print data
		time.sleep(1)
		if not data or data.decode('utf-8') == 'exit':
			break
		sock.send(('Hello, %s') % (data).encode('utf-8'))
	sock.close()
	print 'Connection from %s:%s' % (addr)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.settimeout(120)
s.bind(('localhost', 9999))
s.listen(10)

print 'Waiting for connection...'

while True:
	sock, addr = s.accept()
	t = threading.Thread(target=tcplink, args=(sock, addr))
	t.start()

