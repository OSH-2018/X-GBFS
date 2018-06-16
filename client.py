import socket
HOST = 'GBFS_Socket'

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(HOST)

while True:
    cmd = input("Please input msg:")
    s.send(('0,Create,/aaa/bbb/pathaaaTEST,操作系统.ttt,.ttt,leafz,1:23,1:25,1:24').encode('UTF-8'))
    #s.send(b'0,Unlink,/aaa/bbb/path')
    data = s.recv(1024)
    print(data)

    #s.close()