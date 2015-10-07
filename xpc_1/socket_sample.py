# socket_sample.py
# socket_server.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import json
from agent import getOSinfo, parserSystemInfo

HOST, PORT = "169.254.156.41", 1234

# data = agent.getOSInfo('Linux')
data = json.dumps(parserSystemInfo())

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # received = sock.recv(1024)
    # print data
    sock.sendall(data)

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

print "Sent:     {}".format(data)
print "Received: {}".format(received)