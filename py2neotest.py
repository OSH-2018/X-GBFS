from py2neo import Node, NodeMatcher, Graph

graph = Graph(password='zhanglifu')
matcher = NodeMatcher(graph)
result = list(matcher.match('Person'))
print(result)