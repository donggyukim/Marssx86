#!/bin/env python

import os, sys
import threading
import string
import defn_new

workdir = "/home/vteori/sims/marss"
diskdir = "/data/forDonggyu/disk"
orgdisk = "/home/vteori/disk/spec2006.qcow2"

class ThreadClass(threading.Thread):
  def __init__ (self, itcb, fwd):
    threading.Thread.__init__(self)
    self.itcb = itcb
    self.fwd = fwd

  def run(self):
    tgtdisk = "spec2006.qcow2."+self.fwd

    rsh = "%s %s" % ("rsh", self.itcb)

    print "Disk copy at " + self.itcb
    subcmd1 = "%s %s" % ("cd", diskdir)
    subcmd2 = "%s %s %s" % ("cp", orgdisk, tgtdisk)
    rsh_arg = "\"%s;%s\"" % (subcmd1, subcmd2)
    os.system("%s %s" % (rsh, rsh_arg))
    print "Copy done at" + self.itcb + "\n"

    for workload in defn_new.get_workloads():
      print "Create checkpoint of " + workload + " at " + self.fwd +"\n"
      subcmd1 = "%s %s" % ("cd", workdir)
      subcmd2 = "%s %s %s %s" % ("./chkpt.exp", workload, self.fwd, diskdir+"/"+tgtdisk)
      rsh_arg = "\"%s;%s\"" % (subcmd1, subcmd2)
      os.system("%s %s" % (rsh, rsh_arg))
      print "Complete for " + workload + " at " + self.fwd +"\n"

threads = []

print "Start 1st round\n"
for i in range(1, 10, 1):
  t = ThreadClass("itcb"+string.zfill(i, 2), str(i)+"00T")
  t.start()
  threads.append(t)

for t in threads:
  t.join()
print "1st round finish\n"

print "Start 2nd round\n"
for i in range(1, 10):
  t = ThreadClass("itcb"+string.zfill(i, 2), str(i)+"T")
  t.start()
  threads.append(t)

for t in threads:
  t.join()
print "2nd round finish\n"
