import socket
HOST = 'GBFS_Socket'

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(HOST)

while True:
    cmd = input("Please input msg:")
    s.send(('0,Open,/aaa/bbb/pathaaa,Sat Jun 16 12:59:02 2018,/aaa/bbb/path').encode('UTF-8'))
    #s.send(('0,Open,/aaa/bbb/1112222,Sat Jun 16 12:59:02 2018,/aaa/bbb/pathaaa').encode('UTF-8'))  
    #s.send(('0,Create,/aaa/bbb/1112222,计算机.ppt,.ttt,leafz,1:3,1:25,1:24').encode('UTF-8'))
    #s.send(b'0,Unlink,/aaa/bbb/path')
    data = s.recv(1024)
    print(data)

    #s.close()