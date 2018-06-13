import socket
import py2neo

def NeoHandle(op):
    
    pass

HOST = '127.0.0.1'
PORT = 8088

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print('Server start at: %s:%s' %(HOST, PORT))
print('wait for connection...')

while True:
    conn, addr = s.accept()
    print('Connected by ', addr)

    while True:
        data = conn.recv(100)
        if not data:
            break
        strdata = str(data)
        strdata = strdata[2:-1]
        data_list = strdata.split(',')
        print(data_list)
        NeoHandle(data_list)
        conn.send(b"server received you message.")
