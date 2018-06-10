# GBFS
## 组会时间安排：

1. 周三上午
2. 周末

## 任务

1. fuse 文件系统编写 GBFS `GBFS.py`
2. Socket, `Server.py`
3. 文件属性提取(DBpedia) `GetProperty.py`
4. 命令行脚本 `GBShell.py`
5. 文件过滤——根据后缀、大小（> 4KB)、所有者，在 `GBFS.py` 中实现
6. 相关文件推荐算法 `Recommend.py`
7. 预读在 `GBFS.py` 实现

## 分工

1. 丁峰：1. 5. 7
2. 谢灵江：3
3. 牛田：6
4. 张立夫：2. 4

## 架构

1. `GBFS.py` 中对数据库的操作全部通过 socket 向进程 `Server.py` 发送请求，请求包括文件的以下属性：创建时间，最近读写时间，后缀，用户，路径
2. `Server.py` 中要对新建文件进行新建节点与添加属性，新建的文件要调用 `GetProperty.py` 获取知识图谱（复旦 DBpedia）中相关属性进行添加， `Server.py` 不断从 socket 中读取请求，实现异步数据库操作
3. `GBFS.py` 在 open 后向 `Server.py` 发送请求，请求包括所打开文件时间与路径，`Server.py` 对 log 文件进行读取，判断上一个文件打开时间与当前打开文件时间相差，若小于 100 秒（暂定），则将两文件间加边，边权默认为 1 ，在 log 文件中写入当前打开文件路径和打开时间
4. `GetProperty.py` 中提取文件的知识图谱（复旦 DBpedia）中所具有的属性，将其返回对应的 key，value
5. 命令行脚本 `GBShell.py` 中实现根据属性搜索文件，对文件添加自定属性，删除文件，查看关联文件，查看文件属性，进行相关文件推荐，查看所有已归档文件等等操作
6. 预读操作：在 `GBFS.py` 中 open 中向 `Server.py` 发送请求，在 `Server.py` 中调用 `Recommend.py` 模块得到所打开文件相邻的权值最大的文件，将其映射入内存中，初步设定关系最近的 5 个文件
7. `Recommend.py` 中两个函数，分别被 `GBShell.py` 和 `Server.py` 调用
   - 由 `GBShell.py` 调用查找输入文件相联权值最大的 5 个（暂定）文件，并将文件名编号输出，用户输入对应编号，`Recommend.py` 跳转到对应文件目录
   - 由 `Server.py` 调用查找输入文件相联权值最大的 5 个（暂定）文件，将路径放入 list 作为返回值，由 `Server.py` 进行预读

## API

1. Socket：

   ​	socket打包发送给server.py 每个包固定大小100,内容之间以逗号隔开	

   ​	创建文件时 首先会发出Create 然后是文件路径及其名，文件后缀，uid, atime, mtime, ctime

   ​	读文件时，发出Read和atime

   ​	重命名时，发出Rename，新的文件路径和文件名，文件后缀，新的ctime

   ​	删除文件时，发出Unlink，文件的路径和文件名

   ​	转换所有者时，发出Chown，文件的路径和文件名，新的uid，新的ctime

2. `GetProperty.py` ：
   - input: (str) filename
   - output: (list) key, (list) value（其中序号一一对应）

3. `Recommend.py` ：
   - `def shell()` :
     - input: (str) path
     - output: NULL
     - operation: 跳转到所选择文件目录
   - `def server()` :
     - input: (str) path
     - output: (list) path: ['path', 'path', 'path', 'path', 'path']