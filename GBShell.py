import sys, getopt, os
from py2neo import Graph, NodeMatcher, Relationship, RelationshipMatcher

class Shell:
    graph = Graph(password='zhanglifu')

    def matchpath(self, filepath):
        matcher = NodeMatcher(self.graph)
        result = list(matcher.match(path=filepath))
        return result

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

    def getlabel(self, label):
        strlabel = str(label)
        strlabel = strlabel.split(' ')
        strlabel = strlabel[0].split(':')
        strlabel = strlabel[1:]
        return strlabel

    def test(self, argv):
        try:
            opts, args = getopt.getopt(argv,'-h-s:-l:-r:-a:-d:-f:',['help','show=','showlink=','rec=','add=','delete=','find='])
        except getopt.GetoptError:
            print('input error')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-s', '--show'):
                filename = arg
                print(filename)
                if args != []:
                    print('No filename,please give a correct filename')
                    exit(1)
                filepath = os.path.abspath(os.curdir) + '/' + filename
                print(filepath)
                label = self.matchpath(filepath)
                if label == []:
                    print('No label in Neo4j')
                    exit(1)
                label = label[0]
                strlabel = self.getlabel(label)
                print('Labels:')
                j = 1
                for i in strlabel:
                    print('\t' + str(j) + '.', i)
                    j += 1
                print('Properties:')
                print('\t1. name:  ', label['name'])
                print('\t2. path:  ', label['path'])
                print('\t3. ext:   ', label['ext'])
                print('\t4. ctime: ', label['ctime'])
                print('\t5. mtime: ', label['mtime'])
                print('\t6. atime: ', label['atime'])


            elif opt in ('-l', '--showlink'):
                if args != []:
                    print('No filename,please give a correct filename')
                    exit(1)
                filename = arg
                filepath = os.path.abspath(os.curdir) + '/' + filename
                nodes = self.matchpath(filepath)
                if nodes == []:
                    print('No node in Neo4j')
                    exit(1)
                nodes = nodes[0]
                strlabel = str(nodes)
                strlabel = strlabel.split(' ')
                strlabel = strlabel[0].split(':')
                strlabel = strlabel[1:]
                for label in strlabel:
                    print('Relationship:', label)
                    linknodes = self.matchlabel(label)
                    j = 1
                    for node in linknodes:
                        if node['path'] == filepath:
                            continue
                        print('\t', str(j) + '.', 'path: ', node['path'])
                        j += 1
                

            elif opt in ('-r', '--recommend'):
                if args != []:
                    print('No filename,please give a correct filename')
                    exit(1)
                print('recommend')

            elif opt in ('-a', '--add'):
                if args == []:
                    print('No label,please give a label')
                    exit(1)
                filename = arg
                filenum = len(os.listdir())
                if filenum > 1:
                    node_list = args[filenum-1:]
                    dirs = os.listdir()
                    for node in node_list:
                        for f in dirs:
                            filepath = os.path.abspath(os.curdir) + '/' + f
                            nodes = self.matchpath(filepath)
                            if nodes == []:
                                print('No node in Neo4j')
                                exit(1)
                            nodes = nodes[0]
                            for label in node_list:
                                nodes.add_label(label)
                                self.graph.push(nodes)
                                linknodes = self.matchlabel(label)
                                for node in linknodes:
                                    if node['path'] == filepath:
                                        continue
                                    r = Relationship(nodes, label, node)
                                    self.graph.create(r)
                # 加入 * 功能
                else :
                    filepath = os.path.abspath(os.curdir) + '/' + filename
                    nodes = self.matchpath(filepath)
                    if nodes == []:
                        print('No node in Neo4j')
                        exit(1)
                    nodes = nodes[0]
                    for label in args:
                        nodes.add_label(label)
                        self.graph.push(nodes)
                        linknodes = self.matchlabel(label)
                        for node in linknodes:
                            if node['path'] == filepath:
                                continue
                            r = Relationship(nodes, label, node)
                            self.graph.create(r)
                print('Label add successfully!')


            elif opt in ('-d', '--delete'):    
                if args == []:
                    print('No label,please give a label')
                    exit(1)
                filename = arg
                filepath = os.path.abspath(os.curdir) + '/' + filename
                nodes = self.matchpath(filepath)
                if nodes == []:
                    print('No node in Neo4j')
                    exit(1)
                nodes = nodes[0]
                for label in args:
                    nodes.remove_label(label)
                    self.graph.push(nodes)
                    rels = self.matchrel(nodes, label)
                    for rel in rels:
                        self.graph.separate(rel)
                print('Label delete successfully! (if it exists)')


            elif opt in ('-f', '--find'):
                label = arg.split(':')
                if len(label) == 2:
                    nodes = self.matchper(label[0], label[1])
                    if nodes == 0:
                        print('Wrong Property')
                        exit(1)
                elif len(label) == 1:
                    nodes = self.matchlabel(label[0])
                else:
                    print('Wrong Input(too many properties)')
                    exit(1)
                if args != []:
                    for i in range(len(args)):
                        nodeslen = len(nodes)
                        if nodeslen == 0:
                            break
                        label = args[i].split(':')
                        for j in range(nodeslen):
                            node = nodes.pop(0)
                            if len(label) == 2:
                                if node[label[0]] == label[1]:
                                    nodes.append(node)
                                else:
                                    continue
                            elif len(label) == 1:
                                labels = self.getlabel(node)
                                if labels.count(label[0]) == 1:
                                    nodes.append(node)
                                else:
                                    continue
                if nodes == []:
                    print('Not Found')
                    exit(1)
                else:
                    j = 0
                    for node in nodes:
                        print(str(j + 1) + '.', 'name:', node['name'], '  path:', node['path'])
                        j += 1


                
            else:
                print('''Usage： ./GBShell.py  [OPTION]...  [FILE]...  [LABEL/KEY:value]\n
Description：a command line ，users can operate on this to controll the whole GBFS.\n
\t-a, --add\n
​\t\tAdd a label [LABEL] in the given file [FILE]\n
\t-d, --delete\n
​\t\tDelete the label [LABEL] in the given file [FILE].If the given file doesn't have that\n
\t\tlabel,deleting is invaild,and return a warning signal.\n
​\t-f, --find\n
​\t\tUser gives shell the labels [LABEL] or the proporties [KEY:value],and all the nodes\n
\t\tthat have the given labels or proporties are printed in the screen.If none node\n
\t\tmeets the requirements,Not Found will be returned.\n
\t-h, --help\n
​\t\tShow the help info.\n
\t-l, --showlink\n
​\t\tPrint all the files(nodes) that are adjacent to the given file[FILE].\n
​\t-r, --rec\n
​\t\tRecommend.\n
​\t-s, --show\n
​\t\tPrint all the labels and proporties of the given file [FILE].\n ''')

if __name__ == '__main__':
    sh = Shell()
    sh.test(sys.argv[1:])
