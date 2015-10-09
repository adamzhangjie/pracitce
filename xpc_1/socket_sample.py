# socket_sample.py
# socket_server.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import json
from operate_systeminfo_linux import ServerInfo_linux

HOST, PORT = "12.99.151.180", 1234

# data = agent.getOSInfo('Linux')
server_info = ServerInfo_linux()
server_info.getOrganizedInfo()
data = json.dumps(server_info.server_static_dict_data)

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

print data
print received