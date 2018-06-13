import socket
HOST = 'GBFS_Socket'

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(HOST)

while True:
    cmd = input("Please input msg:")
    s.send(b'0,Create,/aaa/bbb/path,test.ttt,.ttt,leafz,16:23,16:25,16:24')
    #s.send(b'0,Unlink,/aaa/bbb/path')
    data = s.recv(1024)
    print(data)

    #s.close()