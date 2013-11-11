#!/bin/env python

import os
import sys
import errno
import threading
import string

from time import gmtime, strftime

import defn

def make_cfgs(workload, cycles, interval_dir):
  filename = workload+"_"+cycles+".cfg"
  f = open(os.getcwd()+"/cfgs/"+filename,"w")

  ### DEFAULT SETTING ###
  f.write("[DEFAULT]\n")
  f.write("marss_dir = "+os.getcwd()+"\n")
  f.write("util_dir = %(marss_dir)s/util\n")
  f.write("img_dir = /work/vteori/qemu_disk\n")
  f.write("qemu_bin = %(marss_dir)s/qemu/qemu-system-x86_64\n")
  f.write("default_simconfig = -kill-after-run -quiet -run -stopinsns " + cycles + "\n\n")

  f.write("[suite spec2006-int]\n")
  f.write("checkpoints = "+workload+"\n\n")

  ### base ###
  f.write("[run base]\n")
  f.write("suite = spec2006-int\n")
  f.write("images = %(img_dir)s/spec2006_"+defn.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-base.interval\n")
  f.write("  -periodic-interval "+interval_dir+"/%(bench)s-base.pinterval\n")
  f.write("  -interval-insns 1M\n")
  #f.write("  -interval %(out_dir)s/%(bench)s-base.interval\n")
  f.write("  -trace %(out_dir)s/%(bench)s.trace\n\n")

  ### interval ###
  f.write("[run interval]\n")
  f.write("suite = spec2006-int\n")
  f.write("images = %(img_dir)s/spec2006_"+defn.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-base.interval\n")
  f.write("  -periodic-interval "+interval_dir+"/%(bench)s-base.pinterval\n")
  f.write("  -interval-insns 10000\n")
  #f.write("  -interval %(out_dir)s/%(bench)s-base.interval\n")

  ### perfect configurations ###
  for config in defn.configs:
    f.write("[run perf-"+config+"]\n")
    f.write("suite = spec2006-int\n")
    f.write("images = %(img_dir)s/spec2006_"+defn.disk[workload]+".qcow2\n")
    f.write("memory = 4096\n")
    f.write("simconfig = %(default_simconfig)s\n")
    f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
    f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
    f.write("  -machine single_core\n")
    f.write("  -perfect-"+config+"\n")
    f.write("  -interval "+interval_dir+"/%(bench)s-"+config+".interval\n\n")
    #f.write("  -interval %(out_dir)s/%(bench)s-"+config+".interval\n\n")

  ### perfect I$ ###
  f.write("[run perf-icache]\n")
  f.write("suite = spec2006-int\n")
  f.write("images = %(img_dir)s/spec2006_"+defn.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  f.write("  -perfect-l1-icache\n")
  f.write("  -perfect-l2-icache\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-perfect-icache.interval\n\n")

  ### perfect D$ ###
  f.write("[run perf-dcache]\n")
  f.write("suite = spec2006-int\n")
  f.write("images = %(img_dir)s/spec2006_"+defn.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-dtlb\n")
  f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l2-dcache\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-perfect-dcache.interval\n\n")

  ### perfect all ###
  f.write("[run perf-all]\n")
  f.write("suite = spec2006-int\n")
  f.write("images = %(img_dir)s/spec2006_"+defn.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  f.write("  -perfect-l1-icache\n")
  f.write("  -perfect-l2-icache\n")
  #f.write("  -perfect-dtlb\n")
  #f.write("  -perfect-l1-dcache\n")
  #f.write("  -perfect-l2-dcache\n")
  #f.write("  -perfect-branch-pred\n")
  #f.write("  -perfect-long-lat\n")
  f.write("  -trace %(out_dir)s/%(bench)s.trace\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-perfect-all.interval\n\n")

  ### perfect configuration combinations ###
  for configs in defn.config_combs:
    f.write("[run perf-"+string.join(configs,'-')+"]\n")
    f.write("suite = spec2006-int\n")
    f.write("images = %(img_dir)s/spec2006_"+defn.disk[workload]+".qcow2\n")
    f.write("memory = 4096\n")
    f.write("simconfig = %(default_simconfig)s\n")
    f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
    f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
    f.write("  -machine single_core\n")
    f.write("  -interval "+interval_dir+"/%(bench)s-"+string.join(configs,'-')+".interval\n")
    #f.write("  -interval %(out_dir)s/%(bench)s-"+string.join(config,'-')+".interval\n")
    for config in configs:
      f.write("  -perfect-"+config+"\n")
    f.write("\n")
  
  f.close()
  return

### __main__ ###
try:
  cycles = sys.argv[1]
  interval_dir = sys.argv[2]
  os.chdir('../')
  workloads = defn.get_workloads()
  for workload in workloads:
    make_cfgs(workload, cycles, interval_dir)

except IndexError:
  print "Incorrect arguments..."
  print "Usage: ./make_cfgs.py [cycles(e.g. 100M)]"

