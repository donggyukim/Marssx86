#!/bin/env python

import os
import sys
import errno
import threading
import string

from time import gmtime, strftime

import defn

def get_time():
  return "["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"

class ThreadClass(threading.Thread):
  def __init__(self, workload, cycles, config):
    threading.Thread.__init__(self)
    self.workload = workload
    self.cycles = cycles
    self.config = config

  def run(self):
    out_dir = "/work/vteori/results/"+self.workload+"_"+self.config
    cfg_dir = os.getcwd()+"/cfgs/"
    cfg_name = self.workload+"_"+self.cycles+".cfg"

    command = ("util/run_bench.py -d "+out_dir+" -c "+cfg_dir+cfg_name+" "+self.config)
    os.system(command)

### __main___ ###
try:
  os.chdir('../')
  workload = sys.argv[1]
  cycles = sys.argv[2]

  print get_time()+" "+workload+" "+cycles+" starts!"
  
  ### run base producing a trace ###
  threads = []
  base_t = ThreadClass(workload, cycles, "base")
  base_t.start()
  threads.append(base_t)

  ### run perfect configurations ###
  for config in defn.configs:
    t = ThreadClass(workload, cycles, "perf-"+config)
    t.start()
    threads.append(t)

  ### run perfect all ###
  all_t = ThreadClass(workload, cycles, "perf-all")
  all_t.start()
  threads.append(all_t)
  
  for t in threads:
    t.join()

  print get_time()+" "+workload+" "+cycles+"'s 1st round done!"

  """
  threads = []

  for config in defn.simple_configs:
    t = ThreadClass(workload, cycles, "perf-"+config)
    t.start()
    threads.append(t)

  ### run perfect all ###
  all_t = ThreadClass(workload, cycles, "perf-all")
  all_t.start()
  threads.append(all_t)

  for t in threads:
    t.join()

  print get_time()+" "+workload+" "+cycles+"'s 2nd round done!"
  """

except IndexError:
  print "Incorrect arguments..."
  print "Usage: ./one_shot_local.py [workload] [cycles]"
