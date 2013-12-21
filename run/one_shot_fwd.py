#!/bin/env python

import os,sys
import threading
from time import gmtime, strftime

import defn_new

def get_time():
  return "["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"

class ThreadClass(threading.Thread):
  def __init__(self, workload, fwd, insns):
    threading.Thread.__init__(self)
    self.workload = workload
    self.fwd = fwd
    self.insns = insns
    return

  def run(self):
    os.system("rsh itcb" + defn_new.itcb[self.workload] + " \"cd " + os.getcwd() + "; ./one_shot_local.py "+ self.workload + " " + self.insns + " \" ")
    return

### __main__ ###
try:
  insns = sys.argv[1]

  for j in range(1, 10, 1):
    fwd = str(j)+"0T"
    interval_dir = "/home/vteori/cpistacks/intervals/fwd_"+fwd
    if not os.path.exists(interval_dir):
      os.mkdir(interval_dir)
    
    print "Make cfgs..."
    os.system("./make_cfgs_fwd.py "+insns+" "+fwd+" "+interval_dir)

    print get_time() + "Copy disks..."
    os.system("./disk_copy.py " + fwd)
    print get_time() + "Copy done..."    

    workloads = defn_new.workloads
    for group in range(len(workloads)):
      threads = []

      for i in workloads[group]:
        t = ThreadClass(i, fwd, insns)
        t.start()
        threads.append(t)

      for t in threads:
        t.join()

      print (get_time()+" Group "+str(group+1)+" Done!")

    os.system("./merge_fwd_result.py "+interval_dir)
    
except IndexError:
  print "Incorrect arguments..."
  print "Usage: ./one_shot_simple.py [insns]"
