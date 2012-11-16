#!/bin/env python

import os
import sys
import errno
import threading
import string

from time import gmtime, strftime

import defn

fields = [
	"# of uops", 
	"Base cycle", 
	#"I$ hit", 
	"L1 I$ miss", 
	"L2 I$ miss",
	"ITLB miss", 
	#"Frontend miss",
	#"D$ hit",
	"L1 D$ miss",
	"L2 D$ miss",
	"DTLB miss",
	"Long lat miss",
	#"Backend miss",
	"Branch miss",
	"Total miss",
	"Total cycle"]
	
def merge_results(workload, configs):
  paths = []

  try:
    for config in configs:
      if config == "base":
        dir = workload+'_'+config
      else:
        dir = workload+'_perf-'+config
      interval = workload+'-'+config+'.interval'
      paths.append(interval) 

    files = []
 
    for path in paths:
      file = open(path, 'r')
      files.append(file)

    f = open(workload+'.interval', 'w')

    ### write headers ###
    for config in configs:
      f.write('\t'+config)
    f.write('\n')

    ### skip 3 lines ###
    for file in files:
      file.readline()
      file.readline()
      file.readline()

    ### read each field in all files 
    ### and write to the result file
    for field in fields:
      f.write(field)

      for file in files:
        line = file.readline()
        chunks = line.strip().split('\t')
        for i in range(len(chunks)):
          if i == 1:
            f.write('\t'+chunks[i])

      f.write('\n')

    ### close files ###
    f.close()
    for file in files:
      file.close()
  except IOError as e:
    print str(e)

  return
  

### __main__ ###
os.chdir('/home/vteori/intervals')

configs = defn.get_configs(0)

for i in range(1, defn.conf_options):
  comb_configs = defn.get_configs(i)
  [configs.append(string.join(comb_config,'-')) for comb_config in comb_configs]

workloads = defn.get_workloads()

for workload in workloads:
  merge_results(workload, ['base'] + configs)


