#!/usr/bin/env python3
#=========================================================
# File Name : findKilled.py
# Purpose : Find SIGKILL service from system.log and systemlog.gz on mac OS
# Creation Date : 2021-11-22 16:56:13
# Last Modified : 2021-11-22 18:42:49
# Created By :  John Weng 
#=========================================================
import os,sys,re,bz2,gzip
from collections import Counter,OrderedDict


def findFiles(dir,pattern):
    for dirpath, dirnames, filenames in os.walk(dir):
        for subDir  in dirnames:
            findFiles(subDir,pattern)
        else:
            for file in filenames:
                if file.startswith(pattern):
                    yield os.path.join(dirpath,file) 

def openFile(interator):
    for file in interator:
        if file.endswith('.gz'):
            f = gzip.open(file,'rt')
        elif file.endswith('.bz2'):
            f = bz2.open(file,'rt')
        else:
            f = open(file,'rt')
        yield f
        f.close()

def concatenate(fileHandles):
    for f in fileHandles:
        try:
            while True:
                yield next(f)
        except StopIteration:
            pass

def gen_grep(lines,pattern):
    cond = re.compile(pattern)
    for line in lines:
       if cond.search(line):
           foundList = line.split(' ');
           serviceName = re.sub(r'\[.*\]','',foundList[14]) # mds[97]
           yield foundList[0] + ' ' + foundList[1] + ' ' + serviceName

files = findFiles('/var/log','system.log')
lines = openFile(files)
logs = concatenate(lines) 
matched = gen_grep(logs,'(?i)Service exited due to SIGKILL')
counted_log = Counter(matched)
for log in OrderedDict(counted_log.most_common()):
    print(str(counted_log[log]) + ' ' + log,end = '')




