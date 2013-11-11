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
    out_dir = "/tmp/vteori/results/"+self.workload+"_interval"
    cur_dir = os.getcwd()
    cfg_dir = "cfgs/"
    cfg_name = self.workload+"_"+self.cycles+".cfg"
    run_bench = "util/run_bench.py"
    os.system("rsh itcb"+defn.itcb[self.workload]+" \"cd "+cur_dir+" ; "+run_bench+" -d"+out_dir+" -c"+cfg_dir+cfg_name+" interval"+"\"")
    #os.system(run_bench+" -d"+out_dir+" -c"+cfg_dir+cfg_name+" base")
    return


### __main__ ###
try:
  cycles = sys.argv[1]

  print "Make cfgs..."
  interval_dir = "/home/vteori/cpistacks/intervals"
  #interval_dir = "/home/vteori/partial-intervals"
  os.system("./make_cfgs.py "+cycles+" "+interval_dir)
  if not os.path.exists(interval_dir) :
    os.mkdir(interval_dir)

  os.chdir('../')

  workloads = defn.workloads
  for group in range(len(workloads)) :
    print (get_time()+" Group "+str(group+1)+" Start!")

    threads = []

    for i in workloads[group] :
      t = ThreadClass(i, cycles)
      t.start()
      threads.append(t)

    for t in threads :
      t.join()

    print (get_time()+" Group "+str(group+1)+" Done!")

except IndexError:
  print "Incorrect arguments..."
  print "Usage: ./one_shot.py [cycles]"
