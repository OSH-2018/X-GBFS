#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import os.path
import sys
import errno

try:
    from fuse import FUSE, FuseOSError, Operations
except ImportError:
    print('Failed to import fuse module')
    
try:
    import py2neo
except ImportError:
    print('Failed to import py2neo')


class Passthrough(Operations):
    def __init__(self, root):
        self.root = root    

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        ''' 删除文件时，要把Neo4j的数据库里的标签删除 删除文件时先要删除Relationship'''
        full_path = self._full_path(path)
        a = GBFS_graph.find_one(label=full_path)
        if a!=None:
            GBFS_graph.delete(a)
        return os.unlink(full_path)

    def symlink(self, target, name):
        return os.symlink(self._full_path(target), self._full_path(name))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        ''' 文件预读取工作在用户打开一个文件后开始，若文件太大，占用内存过大，则不执行'''
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        ''' 创建文件时 入Neo4j库 用文件大小，文件后缀名，文件所有者分组
            给文件添加标签  '''

        full_path = self._full_path(path)
        fd = os.open(full_path, os.O_RDWR | os.O_CREAT, mode)        
        if GBFS_graph.find_one(label=full_path)==None:
            return fd
        info = os.fstat(fd)
        name_tuple = os.path.splitext(full_path)
        a = py2neo.Node(name_tuple[1],uid=info.st_uid,gid=info.st_gid,atime=info.st_atime
                ,mtime=info.st_mtime,fd=fd,name=full_path)
        GBFS_graph.create(a)
        return fd
        
    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        s = os.read(fh, length)
        # 更新Neo4j中的label数据
        info = os.fstat(fh)
        node = GBFS_graph.find_one(fd=fh)
        node['atime'] = info.st_atime
        GBFS_graph.push(node)
        return s

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)


def main(mountpoint, root):                     # mountpoint 挂载点 root表示fuse filesystem的初始状态.
    global GBFS_graph                
    GBFS_graph = py2neo.Graph(
            "http://localhost:7474/db",
            username="dingfeng",
            password="ding6964712"
    )
    FUSE(Passthrough(root), mountpoint, foreground=True,debug=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])
