import sys, getopt, os
<<<<<<< HEAD
from py2neo import Node, Graph, NodeMatcher
=======
from py2neo import Node, Graph, NodeMatcher, Relationship, RelationshipMatcher
>>>>>>> 7d95eb23abc82c4954ed88171c38a75741f24f5e

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

<<<<<<< HEAD
=======
    def matchrel(self, node, label):
        graph = Graph(password='zhanglifu')
        matcher = RelationshipMatcher(graph)
        result = list(matcher.match({node}, label))
        return result

>>>>>>> 7d95eb23abc82c4954ed88171c38a75741f24f5e
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
<<<<<<< HEAD
=======
                if label == []:
                    print('Wrong Input')
                    exit(1)
>>>>>>> 7d95eb23abc82c4954ed88171c38a75741f24f5e
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

<<<<<<< HEAD
=======

>>>>>>> 7d95eb23abc82c4954ed88171c38a75741f24f5e
            elif opt in ('-l', '--showlink'):
                if args != []:
                    print('Wrong Input')
                    exit(1)
                filename = arg
                filepath = os.path.abspath(os.curdir) + '/' + filename
                nodes = self.matchpath(filepath)
<<<<<<< HEAD
=======
                if nodes == []:
                    print('Wrong Input')
                    exit(1)
>>>>>>> 7d95eb23abc82c4954ed88171c38a75741f24f5e
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
                
<<<<<<< HEAD
=======

>>>>>>> 7d95eb23abc82c4954ed88171c38a75741f24f5e
            elif opt in ('-r', '--recommend'):
                if args != []:
                    print('Wrong Input')
                    exit(1)
                print('recommend')

<<<<<<< HEAD
            elif opt in ('-a', '--add'):
                
                print('add')

            elif opt in ('-d', '--delete'):
                print('delete')
=======

            elif opt in ('-a', '--add'):
                if args == []:
                    print('Wrong Input')
                    exit(1)
                filename = arg
                filepath = os.path.abspath(os.curdir) + '/' + filename
                nodes = self.matchpath(filepath)
                if nodes == []:
                    print('Wrong Input')
                    exit(1)
                nodes = nodes[0]
                graph = Graph(password='zhanglifu')
                for label in args:
                    nodes.add_label(label)
                    graph.push(nodes)
                    linknodes = self.matchlabel(label)
                    for node in linknodes:
                        if node['path'] == filepath:
                            continue
                        r = Relationship(nodes, label, node)
                        graph.create(r)
                print('Label add successfully!')


            elif opt in ('-d', '--delete'):     # 存在问题：会删掉所有边和节点
                if args == []:
                    print('Wrong Input')
                    exit(1)
                filename = arg
                filepath = os.path.abspath(os.curdir) + '/' + filename
                nodes = self.matchpath(filepath)
                if nodes == []:
                    print('Wrong Input')
                    exit(1)
                nodes = nodes[0]
                print(nodes)
                graph = Graph(password='zhanglifu')
                for label in args:
                    nodes.remove_label(label)
                    graph.push(nodes)
                    rels = self.matchrel(nodes, label)
                    print(rels)
                    for rel in rels:
                        graph.separate(rel)
                print('Label delete successfully! (if it exists)')


>>>>>>> 7d95eb23abc82c4954ed88171c38a75741f24f5e
            elif opt in ('-f', '--find'):
                print('find')
            else:
                print("this is help")

if __name__ == '__main__':
    sh = Shell()
    sh.test(sys.argv[1:])