#!/usr/bin/env python3.6
# -*- coding:utf-8 -*-

from __future__ import with_statement

try:
    import os
    import sys
    import errno
    import time
except ImportError:
    print('failed to import os sys errno time')

try:
    import socket
except ImportError:
    print('failed to import socket')

try:
   import recommand
except ImportError as e:
    print(e)
    print('failed to import recommand.py')

try:
    from fuse import FUSE, FuseOSError, Operations
except ImportError: 
    print('failed to import fuse')

def calculate(string):
    l = len(string)
    num = (l+2) // 100
    zero = (num+1)*100-l-2
    return (num,zero)

def time2acs(st_time):
    return time.asctime(time.localtime(st_time))


class Passthrough(Operations):
    def __init__(self, root):
        self.root = root          

    # Helpers
    # =======

    def _full_path(self, partial):
        partial = partial.lstrip("/")
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
        name_tuple = os.path.splitext(full_path)
        ctime = time2acs(os.stat(full_path).st_ctime)
        if name_tuple[1][1:3]=='sw' or not name_tuple[1] or name_tuple[1][-1]=='~':
            return os.chown(full_path, uid, gid)
        (num,zero) = calculate('Chown,'+full_path+','+str(uid)+','+ctime+',')
        s.send((str(num)+','+'Chown,'+full_path+','+
            str(uid)+','+ctime+','+'0'*zero).encode('utf-8'))
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
        unlinkpath=self._full_path(path)
        name_tuple = os.path.splitext(unlinkpath)
        if name_tuple[1][1:3]=='sw' or not name_tuple[1] or name_tuple[1][-1]=='~':
            return os.unlink(unlinkpath)
        (num,zero) = calculate('Unlink,'+unlinkpath+',')
        s.send((str(num)+','+'Unlink,'+unlinkpath+','+'0'*zero).encode('utf-8'))
        return os.unlink(unlinkpath)

    def symlink(self, target, name):
        return os.symlink(self._full_path(target), self._full_path(name))

    def rename(self, old, new):
        oldpath = self._full_path(old)
        newpath = self._full_path(new)
        name_tuple = os.path.split(newpath)
        ext_tuple=os.path.splitext(newpath)
        if ext_tuple[1][1:3]=='sw' or not ext_tuple[1] or ext_tuple[1][-1]=='~':
            return os.rename(oldpath, newpath)
        os.rename(oldpath, newpath)
        ctime = time2acs(os.stat(newpath).st_ctime)
        (num,zero) = calculate('Rename,'+oldpath+','+newpath+','+name_tuple[1]+','+ctime+','+ext_tuple[1]+',')
        s.send((str(num)+','+'Rename,'+oldpath+','+newpath+','+name_tuple[1]+','+
            ext_tuple[1]+','+ctime+','+'0'*zero).encode('utf-8'))
        return None

    def link(self, target, name):
        targetpath=self._full_path(target)
        namepath=self._full_path(name)
        return os.link(targetpath, namepath)

    def utimens(self, path, times=None):
        # 返回文件的访问和修改时间
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        # 打开一个文件时，需要使用推荐算法 把预读取的文件放入内存中
        # 如果文件太大，不宜直接放入内存
        rec = recommand.Recommand()
        full_path = self._full_path(path)
        path_list = rec.server(path)
        path_str = ",".join(path_list)
        fd = os.open(full_path, flags)
        atime = time2acs(os.fstat(fd).st_atime)
        (num,zero) = calculate('Open,'+full_path+','+atime+','+path_str+',')
        s.send((str(num)+','+'Open,'+full_path+','+atime+','+path_str+','+
            '0'*zero).encode('utf-8'))
        return fd

    def create(self, path, mode, fi=None):
        # 在创造文件时，与socket建立联系
        full_path = self._full_path(path)
        name_tuple = os.path.split(full_path)
        ext_tuple = os.path.splitext(full_path)
        
#       filepath = os.path.abspath(os.curdir)+'/'+sys.argv[2]+path[1:]
#       print(filepath)
#       if os.path.isfile(filepath) == False:
        fd = os.open(full_path, os.O_RDWR | os.O_CREAT, mode)        
        info = os.fstat(fd)
        atime = time2acs(info.st_atime) 
        mtime = time2acs(info.st_mtime)
        ctime = time2acs(info.st_ctime)
        if ext_tuple[1][1:3]=='sw' or not ext_tuple[1] or ext_tuple[1][-1]=='~':
            return fd
        (num,zero) = calculate(','*7+'Create'+full_path+name_tuple[1]+','+ext_tuple[1]+
            str(info.st_uid)+str(atime)+str(mtime)+str(ctime))
        s.send((str(num)+','+'Create,'+full_path+','+name_tuple[1]+','+ext_tuple[1]+','+
            str(info.st_uid)+','+atime+','+mtime+','+ctime+','+'0'*zero).encode('utf-8'))
        return fd
#       else:
#           fd = os.open(full_path, os.O_RDWR | os.O_CREAT, mode)        
#           info = os.fstat(fd)
#           atime = time2acs(info.st_atime) 
#           mtime = time2acs(info.st_mtime)
#           ctime = time2acs(info.st_ctime)
#           if ext_tuple[1][1:3]=='sw' or not ext_tuple[1] or ext_tuple[1][-1]=='~':
#               return fd
#           (num,zero) = calculate('Change,'+full_path+','+atime+','+mtime+','+ctime+',')
#           s.send((str(num)+','+'Change,'+full_path+','+atime+','+mtime+','+
#               ctime+','+'0'*zero).encode('utf-8'))
#           return fd
            

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        ret = os.read(fh, length)
        info = os.fstat(fh)
        atime = time2acs(info.st_atime)
        (num,zero) = calculate('Read,'+path+','+atime+',')
        s.send((str(num)+','+'Read,'+path+','+atime+','+'0'*zero).encode('utf-8'))
        return ret 

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


def main(mountpoint, root):
    global s
    address = 'GBFS_Socket'
    s = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    try :
        s.connect(address)
    except socket.error:
        print('socket error')
    FUSE(Passthrough(root), mountpoint, foreground=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])
