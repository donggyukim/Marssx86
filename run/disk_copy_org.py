#!/bin/env python

import os, sys
import threading
import string

#org = "/home/vteori/disk/spec2006.qcow2"
dir = "/work/vteori/qemu_disk"

class ThreadClass(threading.Thread):
  def __init__ (self, itcb, idx):
    threading.Thread.__init__(self)
    self.itcb = itcb
    self.org = "/home/vteori/disk/spec2006_"+str(idx)+".qcow2"

  def run(self):
    print "itcb"+string.zfill(self.itcb, 2)+" start..."
    os.system("rsh itcb"+string.zfill(self.itcb, 2)+" \"cp "+self.org+" "+dir+"\"")
    print "itcb"+string.zfill(self.itcb, 2)+" done..."


for j in range(1, 6):
  print "Copy "+str(j)+"th QEMU disk image..."
  threads = []
  for i in range(1, 15):
    t = ThreadClass(i,j)
    t.start()
    threads.append(t)

  for t in threads:
    t.join()

print "Copy done..."
