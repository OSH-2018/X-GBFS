from py2neo import Node, Graph, NodeMatcher, RelationshipMatcher, Relationship, Database
#from heapq import nlargest
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
    
    def updateweight(self, relationship, value):
        relationship['weight'] = relationship['weight'] + value
        self.graph.push(relationship)

    def shell(self, filepath=None):
        input_node = self.matchpath(filepath)
        strlabel = str(input_node)
        strlabel = strlabel.split(' ')
        strlabel = strlabel[0].split(':')
        strlabel = strlabel[1:]
        relation_list = []
        for label in strlabel:
            rel_list = self.matchrel(input_node, label)
            relation_list.extend(rel_list)# 所有的关系
        # 此处有陷阱：因为这里得到的所有关系是根据label检索的，
        # 然而一个文件节点可以拥有多个label，意味着这里得到的
        # 关系可能是有相同的端点，导致我们推荐算法中有相同的文
        # 件，甚至权值的更新也会出现问题
        # 注：虽然这些关系之间可能两个端点相同，但是这些边之间不会端点、label（r_type）、property都相同。
        #    因为一个两个端点之间的边label必定不相同，label相同的两条边必定端点不相同
        #
        # 解决办法：在上面得到该节点连接的所有关系后，对端点相同的关系进行剔除，留下权值最大的关系
        #
        Neighbor_list_all = []# 所有的相邻节点
        for rel in relation_list:
            nn = rel.nodes
            nn0 = nn[0]
            nn1 = nn[1]
            if nn0 == input_node:
                Neighbor_list_all.append(nn1)
            else:
                Neighbor_list_all.append(nn0)
        # 得到Neighbor_list_all为input_node的所有相邻节点，相邻节点的index与relation的index一致
        Neighbor_index_list = []
        for neighbor in Neighbor_list_all:
            find = neighbor
            Neighbor_index_list.append([i for i,v in enumerate(Neighbor_list_all) if v==find])
        Neighbor_index_list = sorted(set(Neighbor_index_list), key = Neighbor_index_list.index)
        # 得到元素为list的list，list中的list是端点相同的边的index
        new_relation_index_list = []
        for index_list in Neighbor_index_list:
            if len(index_list) == 1:
                new_relation_index_list.append(index_list[0])
            else:
                tem_list = []
                i = 0
                while i < len(index_list):
                    tem_list.append(relation_list[index_list[i]]['weight'])
                    new_relation_index_list.append(tem_list.index(max(tem_list))) 
        new_relation_list = []
        for index in new_relation_index_list:
            new_relation_list.append(relation_list[index])
        # 得到new_relation_list为处理后的、没有端点相同关系的list
        rel_num = len(new_relation_list)
        if rel_num >= 5:
            rel_num = 5
        weight_list = []
        for rel in new_relation_list:
            weight_list.append(rel['weight'])# 提取weight
        # 将weight提取成一个list进行后续操作
        n = rel_num
        index_list = []
        while n > 0:
            index = weight_list.index(max(weight_list))
            index_list.append(index)
            weight_list[index] = 0
            n = n - 1
        m = 0
        relation_top5_list = []
        while m < rel_num:
            relation_top5_list.append(new_relation_list[index_list[m]])
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
        # 接下来两个操作：
        # 1：更新权值weight
        i = 0
        while i < rel_num:
            if i == index:
                if relation_top5_list[i]['weight'] == 10:
                    continue
                else:
                    self.updateweight(relation_top5_list[i], 1)
            else:
                if  relation_top5_list[i]['weight'] >= 6:
                    self.updateweight(relation_top5_list[i], -1)
        # 2: 根据用户输入进入新的工作目录
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
    
    
    
    def server(self, filepath):
        input_node = self.matchpath(filepath)
        strlabel = str(input_node)
        strlabel = strlabel.split(' ')
        strlabel = strlabel[0].split(':')
        strlabel = strlabel[1:]
        relation_list = []
        for label in strlabel:
            rel_list = self.matchrel(input_node, label)
            relation_list.extend(rel_list)# 所有的关系
        # 确认relationship的数量，如果小于三个需要特殊考虑
        Neighbor_list_all = []# 所有的相邻节点
        for rel in relation_list:
            nn = rel.nodes
            nn0 = nn[0]
            nn1 = nn[1]
            if nn0 == input_node:
                Neighbor_list_all.append(nn1)
            else:
                Neighbor_list_all.append(nn0)
        # 得到Neighbor_list_all为input_node的所有相邻节点，相邻节点的index与relation的index一致
        Neighbor_index_list = []
        for neighbor in Neighbor_list_all:
            find = neighbor
            Neighbor_index_list.append([i for i,v in enumerate(Neighbor_list_all) if v==find])
        Neighbor_index_list = sorted(set(Neighbor_index_list), key = Neighbor_index_list.index)
        # 得到元素为list的list，list中的list是端点相同的边的index
        new_relation_index_list = []
        for index_list in Neighbor_index_list:
            if len(index_list) == 1:
                new_relation_index_list.append(index_list[0])
            else:
                tem_list = []
                i = 0
                while i < len(index_list):
                    tem_list.append(relation_list[index_list[i]]['weight'])
                    new_relation_index_list.append(tem_list.index(max(tem_list))) 
        new_relation_list = []
        for index in new_relation_index_list:
            new_relation_list.append(relation_list[index])
        # 得到new_relation_list为处理后的、没有端点相同关系的list
        rel_num = len(new_relation_list)
        if rel_num >= 3:
            rel_num = 3# 当关系数量大于等于3时，限制relationship数量为3
        weight_list = []
        for rel in new_relation_list:
            weight_list.append(rel['weight'])# 提取weight
        # 将weight提取成一个list进行后续操作
        n = rel_num
        index_list = []
        while n > 0:
            index = weight_list.index(max(weight_list))
            index_list.append(index)
            weight_list[index] = 0
            n = n - 1
        m = 0
        relation_top5_list = []
        while m < rel_num:
            relation_top5_list.append(new_relation_list[index_list[m]])
            m = m + 1
        # 得到了相关性最大的5个节点与输入节点之间的关系，通过该关系调用.nodes()可以返
        # 回这5个节点
        Neighbor_list = []
        for relation in relation_top5_list:
            Neighbor_nodes = relation.nodes
            Neighbor_node0 = Neighbor_nodes[0]
            Neighbor_node1 = Neighbor_nodes[1]
            if Neighbor_node0 == input_node:
                Neighbor_list.append(str(Neighbor_node1))
            else:
                Neighbor_list.append(str(Neighbor_node0))
        path_list = []# 用于存储5个关系最大的节点的"path"属性
        for nodes in Neighbor_list:
            path_list.append(nodes['path'])
        return path_list
        



