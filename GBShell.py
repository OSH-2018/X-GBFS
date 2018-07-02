import sys, getopt, os
from py2neo import Graph, NodeMatcher, Relationship, RelationshipMatcher
from recommand import Recommand

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

    def test(self, argv):
        try:
            opts, args = getopt.getopt(argv,'-h-s:-l:-r:-a:-d:-f:',['help','show=','showlink=','rec=','add=','delete=','find='])
        except getopt.GetoptError:
            print('Parameter input error, \'python GBShell.py -h\' look for help')
            sys.exit(2)
        for opt, arg in opts:

            if opt in ('-s', '--show'):
                filename = arg
                filepath = os.path.abspath(os.curdir) + '/' + filename
                files = os.listdir()
                filenum = 1
                for text in args:
                    for f in files:
                        if f == text:
                            if os.path.isdir(f):
                                break
                            filenum += 1
                            break
                dirflag = 0
                k = 0
                if os.path.isdir(arg) and args == []:
                    tempfiles = os.listdir(arg)
                    if tempfiles == []:
                        break
                    files = []
                    for f in tempfiles:
                        if f[0] == '.':
                            continue
                        else:
                            files.append(f)
                    filenum = len(files)
                    dirflag = 1
                    filepath = filepath + '/' + files[k]
                    filename = files[k]
                else:
                    filenum = len(args) + 1
                while k < filenum:
                    if os.path.isdir(filename):
                        if k == len(args):
                            break
                        filename = args[k]
                        filepath = os.path.abspath(os.curdir) + '/' + filename
                        k += 1
                        continue
                    label = self.matchpath(filepath)
                    if label == []:
                        print('No label in Neo4j')
                        exit(1)
                    label = label[0]
                    strlabel = str(label.labels)
                    strlabel = strlabel.split(':')
                    strlabel = strlabel[1:]
                    print('File: ', filename)
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
                    print('\n')
                    if dirflag:
                        if k + 1 == len(files):
                            break
                        filename = files[k + 1]
                        filepath = os.path.abspath(os.curdir) + '/' + arg + '/' + filename
                    else:
                        if k == len(args):
                            break
                        filename = args[k]
                        filepath = os.path.abspath(os.curdir) + '/' + filename
                    k += 1


            elif opt in ('-l', '--showlink'):
                filename = arg
                filepath = os.path.abspath(os.curdir) + '/' + filename
                files = os.listdir()
                filenum = 1
                for text in args:
                    for f in files:
                        if f == text:
                            if os.path.isdir(f):
                                break
                            filenum += 1
                            break
                dirflag = 0
                i = 0
                if os.path.isdir(arg) and args == []:
                    tempfiles = os.listdir(arg)
                    if tempfiles == []:
                        break
                    files = []
                    for f in tempfiles:
                        if f[0] == '.':
                            continue
                        else:
                            files.append(f)
                    filenum = len(files)
                    dirflag = 1
                    filename = files[i]
                    filepath = filepath + '/' + files[i]
                else:
                    filenum = len(args) + 1
                while i < filenum:
                    if os.path.isdir(filename):
                        if i == len(args):
                            break
                        filename = args[i]
                        filepath = os.path.abspath(os.curdir) + '/' + filename
                        i += 1
                        continue
                    nodes = self.matchpath(filepath)
                    if nodes == []:
                        print('No node in Neo4j')
                        exit(1)
                    nodes = nodes[0]
                    strlabel = str(nodes.labels)
                    strlabel = strlabel.split(':')
                    strlabel = strlabel[1:]
                    print('File: ', filename)
                    for label in strlabel:
                        print('Relationship:', label)
                        linknodes = self.matchlabel(label)
                        j = 1
                        for node in linknodes:
                            if node['path'] == filepath:
                                continue
                            print('\t', str(j) + '.', 'path: ', node['path'])
                            j += 1
                    print('\n')
                    if dirflag:
                        if i + 1 == len(files):
                            break
                        filename = files[i + 1]
                        filepath = os.path.abspath(os.curdir) + '/' + arg + '/' + filename
                    else:
                        if i == len(args):
                            break
                        filename = args[i]
                        filepath = os.path.abspath(os.curdir) + '/' + filename
                    i += 1
                

            elif opt in ('-r', '--recommend'):
                if args != []:
                    print('Too many parameters')
                    exit(1)
                filename = arg
                path = os.path.abspath(os.curdir) + '/' + filename
                rc = Recommand()
                rc.shell(filepath=path)
                print('Recommend finish!')

            elif opt in ('-a', '--add'):
                if args == []:
                    print('Least one label should be given')
                    exit(1)
                filename = arg
                filepath = os.path.abspath(os.curdir) + '/' + filename
                files = os.listdir()
                if os.path.isdir(arg):
                    filenum = 0
                    dirnum = 1
                else:
                    filenum = 1
                    dirnum = 0
                for test in args:
                    for f in files:
                        if f == test:
                            if os.path.isdir(f):
                                dirnum += 1
                                break
                            filenum += 1
                            break
                print(filenum, dirnum)
                labels = args[filenum + dirnum -1:]
                print(labels)
                dirflag = 0
                i = 0
                if os.path.isdir(arg) and not os.path.isdir(args[0]) and not os.path.isfile(args[0]):
                    tempfiles = os.listdir(arg)
                    if tempfiles == []:
                        break
                    files = []
                    for f in tempfiles:
                        if f[0] == '.':
                            continue
                        else:
                            files.append(f)
                    filenum = len(files)
                    dirflag = 1
                    filename = files[i]
                    filepath = filepath + '/' + files[i]
                while i < filenum + dirnum:
                    if os.path.isdir(filename):
                        if i == len(args):
                            break
                        filename = args[i]
                        filepath = os.path.abspath(os.curdir) + '/' + filename
                        i += 1
                        continue
                    nodes = self.matchpath(filepath)
                    if nodes == []:
                        print('No node in Neo4j')
                        exit(1)
                    nodes = nodes[0]
                    for label in labels:
                        if nodes.has_label(label):
                            break
                        nodes.add_label(label)
                        self.graph.push(nodes)
                        linknodes = self.matchlabel(label)
                        for node in linknodes:
                            if node['path'] == filepath:
                                continue
                            r = Relationship(nodes, label, node)
                            r['weight'] = 1
                            self.graph.create(r)
                    if dirflag:
                        if i + 1 == len(files):
                            break
                        filename = files[i + 1]
                        filepath = os.path.abspath(os.curdir) + '/' + arg + '/' + filename
                    else:
                        filename = args[i]
                        filepath = os.path.abspath(os.curdir) + '/' + filename
                    i += 1
                print('Label added successfully!')


            elif opt in ('-d', '--delete'):    
                if args == []:
                    print('Least one label should be given')
                    exit(1)
                filename = arg
                filepath = os.path.abspath(os.curdir) + '/' + filename
                files = os.listdir()
                if os.path.isdir(arg):
                    filenum = 0
                    dirnum = 1
                else:
                    filenum = 1
                    dirnum = 0
                for text in args:
                    for f in files:
                        if f == text:
                            if os.path.isdir(f):
                                dirnum += 1
                                break
                            filenum += 1
                            break
                labels = args[filenum + dirnum -1:]
                dirflag = 0
                i = 0
                if os.path.isdir(arg) and not os.path.isdir(args[0]) and not os.path.isfile(args[0]):
                    tempfiles = os.listdir(arg)
                    if tempfiles == []:
                        break
                    files = []
                    for f in tempfiles:
                        if f[0] == '.':
                            continue
                        else:
                            files.append(f)
                    filenum = len(files)
                    dirflag = 1
                    filename = files[i]
                    filepath = filepath + '/' + files[i]
                while i < filenum + dirnum:
                    if os.path.isdir(filename):
                        if i == len(args):
                            break
                        filename = args[i]
                        filepath = os.path.abspath(os.curdir) + '/' + filename
                        i += 1
                        continue
                    nodes = self.matchpath(filepath)
                    if nodes == []:
                        print('No node in Neo4j')
                        exit(1)
                    nodes = nodes[0]
                    for label in labels:
                        print('delete label: ', label)
                        nodes.remove_label(label)
                        self.graph.push(nodes)
                        rels = self.matchrel(nodes, label)
                        for rel in rels:
                            self.graph.separate(rel)
                    if dirflag:
                        if i + 1 == len(files):
                            break
                        filename = files[i + 1]
                        filepath = os.path.abspath(os.curdir) + '/' + arg + '/' + filename
                    else:
                        if i == len(args):
                            break
                        filename = args[i]
                        filepath = os.path.abspath(os.curdir) + '/' + filename
                    i += 1
                print('Label deleted successfully! (if it exists)')


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
                                labels = str(node.labels)
                                labels = strlabel.split(':')
                                labels = strlabel[1:]
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
                        print('\t' + str(j + 1) + '.', 'name:', node['name'], '\tpath:', node['path'])
                        j += 1
                index = input('Please select the file to open: ')
                try:
                    os.system('open ' + nodes[int(index) - 1]['path'])
                except:
                    print('No such file')


                
            else:
                print('''Usage： ./GBShell.py  [OPTION]...  [FILE]...  [LABEL/KEY:value]\n
Description：a command line ，users can operate on this to controll the whole GBFS.\n
\t-a, --add\n
​\t\tAdd a label [LABEL] or a few labels [LABEL1]...[LABELn] in the given file [FILE].\n
\t\tInput sample:\n
\t\t-a [FILE] [LABEL1] [LABEL2] ... [LABELn]\n
​\t-s, --show\n
​\t\tGive a file [FILE] or a few files [FILE1]...[FILEn],\n
\t\tPrint all the labels and proporties.\n 
\t\tInput sample:\n
\t\t-s [FILE1] [FILE2]...[FILEn]\n
\t-d, --delete\n
​\t\tDelete a label [LABEL] or some labels [LABEL1]...[LABELn] in the given file [FILE].\n
\t\tIf the given file doesn't have [LABEL],deleting is invaild,and return a warning signal.\n
\t\tInput sample:\n
\t\t-d [FILE] [LABEL1] [LABEL2] ... [LABELn]\n
​\t-f, --find\n
​\t\tUser gives shell the labels [LABEL] or the proporties [KEY:value],and all the nodes\n
\t\tthat have the given labels or proporties are printed in the screen.If none node\n
\t\tmeets the requirements,Not Found will be returned.\n
\t\tInput sample:\n
\t\t-f [LABEL1] [LABEL2] [KEY1:value1] [LABEL3] [key2:value2]\n
\t-l, --showlink\n
​\t\tPrint all the files(nodes) that are adjacent to the given file [FILE].\n
\t\tInput sample:\n
\t\t-l [FILE1] [FILE2]...[FILEn]\n
​\t-r, --rec\n
​\t\tRecommend a few files which may have relation with the given flie [FILE].\n
​\t\tYou can choose the file you want to open.\n
\t\tInput sample:\n
\t\t-r [FILE]\n
\t-h, --help\n
​\t\tShow the help info.\n''')

if __name__ == '__main__':
    sh = Shell()
    sh.test(sys.argv[1:])
