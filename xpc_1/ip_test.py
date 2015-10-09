# ip_test.py
import socket
myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)
print myaddr