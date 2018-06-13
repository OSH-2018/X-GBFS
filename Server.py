import socket
from py2neo import Graph, Node, NodeMatcher, Relationship, RelationshipMatcher
import os

class Server:
    graph = Graph(password='zhanglifu')

    def matchlabel(self, label):
        matcher = NodeMatcher(self.graph)
        result = list(matcher.match(label))
        return result

    def matchrel(self, node, label):
        matcher = RelationshipMatcher(self.graph)
        result = list(matcher.match({node}, label))
        return result

    def matchper(self, key, value):
        if key == 'name':
            result = list(self.graph.nodes.match(name=value))
        elif key == 'path':
            result = list(self.graph.nodes.match(path=value))
        elif key == 'ext':
            result = list(self.graph.nodes.match(ext=value))
        else:
            result = 0
        return result

    def NeoHandle(self, op):
        op.pop(0)
        if op[0] == 'Create':
            nodes = Node(name=op[2], path=op[1], ext=op[3], uid=op[4], atime=op[5], mtime=op[6], ctime=op[7])
            labels = ['Person', 'Thing', 'leafz']
            self.graph.create(nodes)
            for label in labels:
                print('label: ', label)
                nodes.add_label(label)
                self.graph.push(nodes)
                linknodes = self.matchlabel(label)
                for node in linknodes:
                    if node['path'] == op[1]:
                        continue
                    r = Relationship(nodes, label, node)
                    self.graph.create(r)

        elif op[0] == 'Read':
            nodes = self.matchper('path', op[1])
            node = nodes[0]
            node['atime'] = op[2]
            self.graph.push(node)

        elif op[0] == 'Rename':
            nodes = self.matchper('path', op[1])
            node = nodes[0]
            node['path'] = op[2]
            node['name'] = op[3]
            node['ext'] = op[4]
            node['ctime'] = op[5]
            self.graph.push(node)

        elif op[0] == 'Unlink':
            nodes = self.matchper('path', op[1])
            node = nodes[0]
            print(node)
            self.graph.delete(node)

        elif op[0] == 'Chown':
            nodes = self.matchper('path', op[1])
            node = nodes[0]
            node['uid'] = op[2]
            node['ctime'] = op[3]
            self.graph.push(node)
        
        elif op[0] == 'Change':
            nodes = self.matchper('path', op[1])
            node = nodes[0]
            node['atime'] = op[2]
            node['mtime'] = op[3]
            node['ctime'] = op[4]
            self.graph.push(node)
            
        else:
            return


if __name__ == '__main__':
    HOST = 'GBFS_Socket'
    
    try:
        os.unlink(HOST)
    except OSError:
        if os.path.exists(HOST):
            raise
    
    
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(HOST)
    s.listen(2)
    
    print('Server start at: %s:' %HOST)
    print('wait for connection...')
    
    while True:
        conn, addr = s.accept()
        print('Connected by ', addr)
    
        while True:
            data = conn.recv(100)
            print(data)
            if not data:
                break
            strdata = str(data)
            strdata = strdata[2:-1]
            if strdata[0] != '0':
                for i in range(int(strdata[0])):
                    data = conn.recv(100)
                    strdata_temp = str(data)
                    strdata_temp = strdata_temp[2:-1]
                    strdata = strdata + strdata_temp
    
            data_list = strdata.split(',')
            print(data_list)
            handle = Server()
            handle.NeoHandle(data_list)
            conn.send(b"server received you message.")
    