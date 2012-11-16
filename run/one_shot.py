#!/bin/env python

import os,sys
import threading
from time import gmtime, strftime

import defn

def get_time():
  return "["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"

class ThreadClass(threading.Thread):
  def __init__(self, workload, cycle):
    threading.Thread.__init__(self)
    self.workload = workload
    self.cycles = cycles
    return

  def run(self):
    os.system("rsh itcb" + defn.itcb[self.workload] + " \"cd " + os.getcwd() + "; ./one_shot_local.py "+ self.workload + " " + self.cycles+" \" ")
    return


### __main__ ###
try:
  cycles = sys.argv[1]

  print "Make cfgs..."
  os.system("./make_cfgs.py "+cycles+" /home/vteori/intervals")

  workloads = defn.workloads
  for group in range(len(workloads)) :
    print (get_time()+" Group "+str(group)+" Start!")

    threads = []

    for i in workloads[group] :
      t = ThreadClass(i, cycles)
      t.start()
      threads.append(t)

    for t in threads :
      t.join()

    print (get_time()+" Group "+str(group)+" Done!")

except IndexError:
  print "Incorrect arguments..."
  print "Usage: ./one_shot.py [cycles]"
