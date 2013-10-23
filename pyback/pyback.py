#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os 
import datetime, time
import tarfile

class General:
    def __init__(self, dirback, dirdrop):
	self.backup = dirback
	self.dropbox = dirdrop
obj1 = General("/root/BACKUP","/root/Dropbox/")

print obj1.backup, obj1.dropbox
#directory = os.path.dirname(obj1.dropbox)
#contents = os.listdir(directory)
#print contents
now_time = datetime.datetime.now()
now_time = now_time.strftime("%d.%m.%Y-%I.%M")
fileback = "backup%s.tar.gz" % str(now_time)
tar = tarfile.open(fileback, "w:gz")
for root, dir, files in os.walk(obj1.dropbox.decode("utf-8")):
    for file in files:
	fullpath = os.path.join(root, file)
	print root, file
	tar.add(fullpath)
tar.close()