import socket
from py2neo import Graph, Node, NodeMatcher, Relationship, RelationshipMatcher
import os
import GetProperty as gp
import time

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

    def relmatcher(self, node1, node2):
        matcher = RelationshipMatcher(self.graph)
        result = list(matcher.match({node1, node2}))
        return result

    def NeoHandle(self, op, filedict):
        op.pop(0)
        if op[0] == 'Create':
            tempnode = self.matchper('path', op[1])
            if tempnode == []:
                nodes = Node(name=op[2], path=op[1], ext=op[3], uid=op[4], atime=op[5], mtime=op[6], ctime=op[7])
                filename = op[2].split('.')
                filename = filename[0]
                print('filename: ', filename)
                labels = gp.getproperty(filename)
                self.graph.create(nodes)
                if labels[0] == 'OK':
                    labels.pop(0)
                    for label in labels:
                        print('label: ', label)
                        nodes.add_label(label)
                        self.graph.push(nodes)
                        linknodes = self.matchlabel(label)
                        for node in linknodes:
                            if node['path'] == op[1]:
                                continue
                            r = Relationship(nodes, label, node)
                            r['weight'] = 1
                            self.graph.create(r)
            else:
                tempnode = tempnode[0]
                tempnode['ext'] = op[3]
                tempnode['atime'] = op[5]
                tempnode['mtime'] = op[6]
                tempnode['ctime'] = op[7]
                self.graph.push(tempnode)
        
        elif op[0] == 'Open':
            print('ops: ', op)
            nodes = self.matchper('path', op[1])
            if nodes == []:
                print('Wrong op')
                return
            prefetch = op[3:]
            for prefile in prefetch:
                if os.path.exists(prefile):
                    size = os.path.getsize(prefile)
                    fd = os.open(prefile, os.O_RDONLY)
                    if size < 4 * 1024 * 1024:
                        os.read(fd, size)
                    else:
                        os.read(fd, 4 * 1024 * 1024)
                    os.close(fd)
            opentime = time.mktime(time.strptime(op[2], '%a %b %d %H:%M:%S %Y'))
            print('filedict: ', filedict)
            if abs(filedict['time'] - opentime) < 100:
                if filedict['file1'] == op[1] or filedict['file2'] == op[1] or filedict['file3'] == op[1]:
                    lastfile = filedict['initfile']
                    node1 = self.matchper('path', lastfile)
                    node1 = node1[0]
                    node2 = nodes[0]
                    rels = self.relmatcher(node1, node2)
                    for rel in rels:
                        if rel['weight'] < 10:
                            rel['weight'] += 1
                            self.graph.push(rel)
                    for i in range(3):
                        if filedict['file' + str(i + 1)] == op[1] or filedict['file' + str(i + 1)] == '':
                            continue
                        else:
                            node3 = self.matchper('path', filedict['file' + str(i + 1)])
                            if node3 == []:
                                print('Wrong input')
                                continue
                            node3 = node3[0]
                            rels = self.relmatcher(node1, node3)
                            print(rels)
                            for rel in rels:
                                if rel['weight'] >= 6:
                                    rel['weight'] -= 1
                                    self.graph.push(rel)
            node = nodes[0]
            node['atime'] = op[2]
            filedict['initfile'] = op[1]
            filedict['time'] = opentime
            for j in range(3):
                if j + 3 < len(op):
                    filedict['file' + str(j + 1)] = op[j + 3]
            self.graph.push(node)

        elif op[0] == 'Read':
            nodes = self.matchper('path', op[1])
            if nodes == []:
                print('Wrong op')
                return
            node = nodes[0]
            node['atime'] = op[2]
            self.graph.push(node)

        elif op[0] == 'Rename':
            nodes = self.matchper('path', op[1])
            if nodes == []:
                print('Wrong op')
                return
            node = nodes[0]
            node['path'] = op[2]
            node['name'] = op[3]
            node['ext'] = op[4]
            node['ctime'] = op[5]
            self.graph.push(node)

        elif op[0] == 'Unlink':
            if filedict['initfile'] == op[1]:
                filedict['initfile'] = ''
                for j in range(3):
                    filedict['file' + str(j + 1)] = ''
                filedict['time'] = 0.0
            for j in range(3):
                if filedict['file' + str(j + 1)] == op[1]:
                    filedict['file' + str(j + 1)] = ''

            nodes = self.matchper('path', op[1])
            if nodes == []:
                print('Wrong op')
                return
            node = nodes[0]
            print(node)
            self.graph.delete(node)

        elif op[0] == 'Chown':
            nodes = self.matchper('path', op[1])
            if nodes == []:
                print('Wrong op')
                return
            node = nodes[0]
            node['uid'] = op[2]
            node['ctime'] = op[3]
            self.graph.push(node)
        
        elif op[0] == 'Change':
            nodes = self.matchper('path', op[1])
            if nodes == []:
                print('Wrong op')
                return
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
    
    filedict = {'initfile':'', 'file1':'', 'file2':'', 'file3':'', 'time':1529125142.0}

    while True:
        conn, addr = s.accept()
        print('Connected by ', addr)
    
        while True:
            data = conn.recv(100)
            strdata = data.decode('UTF-8')
            print(data)
            if not data:
                break
            print(strdata[0])
            if strdata[0] != '0':
                for i in range(int(strdata[0])):
                    data = conn.recv(100)
                    strdata_temp = data.decode('UTF-8')
                    strdata = strdata + strdata_temp
    
            data_list = strdata.split(',')
            print(data_list)
            handle = Server()
            handle.NeoHandle(data_list, filedict)
            conn.send(b"server received you message.")
    