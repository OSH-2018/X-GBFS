import sys, getopt, os
from py2neo import Node, Graph, NodeMatcher

class Shell:
    def matchpath(self, filepath):
        graph = Graph(password='zhanglifu')
        matcher = NodeMatcher(graph)
        result = list(matcher.match(path=filepath))
        return result

    def matchlabel(self, label):
        graph = Graph(password='zhanglifu')
        matcher = NodeMatcher(graph)
        result = list(matcher.match(label))
        return result

    def test(self, argv):
        try:
            opts, args = getopt.getopt(argv,'-h-s:-l:-r:-a:-d:-f:',['help','show=','showlink=','rec=','add=','delete=','find='])
            print('args: ', args)
        except getopt.GetoptError:
            print('input error')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-s', '--show'):
                filename = arg
                if args != []:
                    print('Wrong Input')
                    exit(1)
                filepath = os.path.abspath(os.curdir) + '/' + filename
                label = self.matchpath(filepath)
                label = label[0]
                strlabel = str(label)
                strlabel = strlabel.split(' ')
                strlabel = strlabel[0].split(':')
                strlabel = strlabel[1:]
                print('Labels:')
                for i in strlabel:
                    print(i)
                print('Properties:')
                print('name: ', label['name'])
                print('path: ', label['path'])
                print('like: ', label['like'])

            elif opt in ('-l', '--showlink'):
                if args != []:
                    print('Wrong Input')
                    exit(1)
                filename = arg
                filepath = os.path.abspath(os.curdir) + '/' + filename
                nodes = self.matchpath(filepath)
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
                        print('\t', j, '. path: ', node['path'])
                        j += 1
                
            elif opt in ('-r', '--recommend'):
                if args != []:
                    print('Wrong Input')
                    exit(1)
                print('recommend')

            elif opt in ('-a', '--add'):
                
                print('add')

            elif opt in ('-d', '--delete'):
                print('delete')
            elif opt in ('-f', '--find'):
                print('find')
            else:
                print("this is help")

if __name__ == '__main__':
    sh = Shell()
    sh.test(sys.argv[1:])