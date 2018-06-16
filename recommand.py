from py2neo import Node, Graph, NodeMatcher, RelationshipMatcher, Relationship, Database
from heapq import nlargest
import os, sys, getopt
#import os
#获取当前工作目录
#>>>os.getcwd()
#更改当前工作目录
#>>>os.chdir('d:\')
#>>>os.getcwd()

class Recommand:
    graph = Graph(password='neo4j')
    
    def matchpath(self, filepath):
        matcher = NodeMatcher(self.graph)
        result = list(matcher.match(path=filepath))
        return result

    def matchrel(self, node, label):
        matcher = RelationshipMatcher(self.graph)
        result = list(matcher.match({node},label))
        return result
    
    def matchlabel(self, label):
        matcher = NodeMatcher(self.graph)
        result = list(matcher.match(label))
        return result

    def shell(self, filepath=None, index=1):
        input_node = self.matchpath(filepath)
        strlabel = str(input_node)
        strlabel = strlabel.split(' ')
        strlabel = strlabel[0].split(':')
        strlabel = strlabel[1:]
        relation_list = []
        for label in strlabel:
            rel_list = self.matchrel(input_node, label)
            relation_list.extend(rel_list)# 所有的关系
        weight_list = []
        for rel in relation_list:
            weight_list.append(rel['weight'])# 提取weight
        # 将weight提取成一个list进行后续操作
        n = 5
        index_list = []
        while n > 0:
            index = weight_list.index(max(weight_list))
            index_list.append(index)
            weight_list[index] = 0
            n = n - 1
        m = 0
        relation_top5_list = []
        while m < 5:
            relation_top5_list.append(relation_list[index_list[m]])
            m = m + 1
        Neighbor_list = []
        for relation in relation_top5_list:
            # 对得到的关系list进行操作提取出输入node的邻点
            Neighbor_nodes = relation.nodes
            Neighbor_node0 = Neighbor_nodes[0]
            Neighbor_node1 = Neighbor_nodes[1]
            if Neighbor_node0 == input_node:
                Neighbor_list.append(str(Neighbor_node1))
            else:
                Neighbor_list.append(str(Neighbor_node0))
        i = 1
        print("GBFS file recommand service: ")
        for Neighbor_node in Neighbor_list:
            print(i,':',Neighbor_node)
        print("\nPlease select the file: ")
        index =int(input())-1 #将输入转换为list下标
        print("your selection: ")
        print(Neighbor_list[index])
        target_node_str = Neighbor_list[index]
        target_node_str = target_node_str.split(' ')
        target_node_str = target_node_str[1:]
        for split_parts in target_node_str:
            if split_parts == 'path:':
                target_path = target_node_str[target_node_str.index('path:')+1]
        target_path = target_path.split('\'')# 使用转义字符 注意
        target_path =  target_path[1]
        #os.getcwd# 获取当前工作目录
        os.chdir(target_path)# 转到了目标目录