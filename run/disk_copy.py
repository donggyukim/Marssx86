#!/bin/env python

import os, sys
import threading
import string

#org = "/home/vteori/disk/spec2006.qcow2"
dir = "/work/vteori/qemu_disk"

class ThreadClass(threading.Thread):
  def __init__ (self, itcb, fwd):
    threading.Thread.__init__(self)
    self.itcb = itcb
    self.org = "/data/forDonggyu/disk/spec2006.qcow2."+fwd

  def run(self):
    print "itcb"+string.zfill(self.itcb, 2)+" start..."
    #os.system("rsh itcb"+string.zfill(self.itcb, 2)+" \"mkdir /work/vteori/\"")
    #os.system("rsh itcb"+string.zfill(self.itcb, 2)+" \"rm -rf /work/vteori/results/*\"")
    os.system("rsh itcb"+string.zfill(self.itcb, 2)+" \"cp "+self.org+" "+dir+"\"")
    print "itcb"+string.zfill(self.itcb, 2)+" done..."

print "Copy QEMU disk images..."

fwd = sys.argv[1];

threads = []

for i in range(1, 15):
  t = ThreadClass(i,fwd)
  t.start()
  threads.append(t)

for t in threads:
  t.join()

print "Copy done..."
