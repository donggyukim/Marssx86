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
        if range(len(chuncks)) == 0:
          f.write('\t0')

      f.write('\n')

    ### close files ###
    f.close()
    for file in files:
      file.close()
  except IOError as e:
    print str(e)

  return
  

### __main__ ###
os.chdir('/home/vteori/cpistacks/intervals')


configs = ['base', 'all'] + defn.configs + defn.config_combs;
workloads = defn.get_workloads()

for workload in workloads:
  merge_results(workload, configs)


