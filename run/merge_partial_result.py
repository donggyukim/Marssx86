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
	
def merge_results(file, workload):
  try:
    f = open(workload+'-base.interval', 'r')
 
    ### skip 3 lines ###
    f.readline()
    f.readline()
    f.readline()

    ### read each field in all files 
    ### and write to the result file
    for field in fields:
      if field == "# of uops" or field == "Total cycle":
        line = f.readline()
        chunks = line.strip().split('\t')
        for i in range(len(chunks)):
          if i == 1:
            file.write(chunks[i]+'\t')
      else:
        f.readline()

    file.write('\n')    
		
    f.close()

  except IOError as e:
    print str(e)

  return
  

### __main__ ###
os.chdir('/home/vteori/partial-intervals')

file = open('result.interval', 'w')
workloads = defn.get_workloads()

for workload in workloads:
  merge_results(file, workload)

file.close()
