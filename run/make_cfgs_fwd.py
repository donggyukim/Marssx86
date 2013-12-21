#!/bin/env python

import os
import sys
import errno
import threading
import string

from time import gmtime, strftime

import defn_new

def make_cfgs(workload, insns, fwd, interval_dir):
  filename = workload+"_"+insns+".cfg"
  f = open(os.getcwd()+"/cfgs/"+filename,"w")

  ### DEFAULT SETTING ###
  f.write("[DEFAULT]\n")
  f.write("marss_dir = "+os.getcwd()+"\n")
  f.write("util_dir = %(marss_dir)s/util\n")
  f.write("img_dir = /work/vteori/qemu_disk\n")
  #f.write("img_dir = /data/forDonggyu\n")
  f.write("qemu_bin = %(marss_dir)s/qemu/qemu-system-x86_64\n")
  f.write("default_simconfig = -kill-after-run -run -quiet -warmup-insns 10M -stopinsns " + insns + "\n\n")
  #f.write("default_simconfig = -kill-after-run -run -quiet -stopinsns " + insns + "\n\n")

  f.write("[suite spec2006]\n")
  f.write("checkpoints = "+workload+"\n\n")

  ### base ###
  f.write("[run base]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-base.interval\n")
  #f.write("  -periodic-interval "+interval_dir+"/%(bench)s-base.pinterval\n")
  #f.write("  -interval %(out_dir)s/%(bench)s-base.interval\n")
  #f.write("  -trace %(out_dir)s/%(bench)s.trace\n\n")

  ### interval ###
  f.write("[run interval]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-interval.interval\n\n")
  #f.write("  -periodic-interval "+interval_dir+"/%(bench)s-base.pinterval\n")
  #f.write("  -interval-insns 1000\n")

  ### perfect configurations ###
  for config in defn_new.configs:
    f.write("[run perf-"+config+"]\n")
    f.write("suite = spec2006\n")
    #f.write("images = %(img_dir)s/spec2006.qcow2\n")
    f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
    #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
    f.write("memory = 4096\n")
    f.write("simconfig = %(default_simconfig)s\n")
    f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
    f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
    f.write("  -machine single_core\n")
    f.write("  -perfect-"+config+"\n")
    f.write("  -interval "+interval_dir+"/%(bench)s-"+config+".interval\n\n")

  ### perfect I$ ###
  f.write("[run perf-icache]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  f.write("  -perfect-l1-icache\n")
  f.write("  -perfect-l2-icache\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-icache.interval\n\n")

  ### perfect frontend ###
  f.write("[run perf-frontend]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  f.write("  -perfect-l1-icache\n")
  f.write("  -perfect-l2-icache\n")
  f.write("  -perfect-branch-pred\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-frontend.interval\n\n")

  ### perfect D$ ###
  f.write("[run perf-dcache]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-dtlb\n")
  f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l2-dcache\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-dcache.interval\n\n")

  ### perfect backend ###
  f.write("[run perf-backend]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-dtlb\n")
  f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l2-dcache\n")
  f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-backend.interval\n\n")

  ### perfect br + l1d ###
  f.write("[run perf-br-l1d]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-branch-pred\n")
  f.write("  -perfect-l1-dcache\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-br-l1d.interval\n\n")

  ### perfect br + l2d ###
  f.write("[run perf-br-l2d]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-branch-pred\n")
  f.write("  -perfect-l2-dcache\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-br-l2d.interval\n\n")

  ### perfect br + dtlb ###
  f.write("[run perf-br-dtlb]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-branch-pred\n")
  f.write("  -perfect-l2-dtlb\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-br-dtlb.interval\n\n")

  ### perfect br + long-lat ###
  f.write("[run perf-br-long-lat]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-branch-pred\n")
  f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-br-long-lat.interval\n\n")

  ### perfect br + backend ###
  f.write("[run perf-br-backend]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-branch-pred\n")
  f.write("  -perfect-dtlb\n")
  f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l2-dcache\n")
  f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-br-backend.interval\n\n")

  ### perfect all ###
  f.write("[run perf-all]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  f.write("  -perfect-l1-icache\n")
  f.write("  -perfect-l2-icache\n")
  f.write("  -perfect-dtlb\n")
  f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l2-dcache\n")
  f.write("  -perfect-branch-pred\n")
  f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-all.interval\n\n")

  ### base1 : l1 dcache ###
  f.write("[run base1]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  f.write("  -perfect-l1-icache\n")
  f.write("  -perfect-l2-icache\n")
  f.write("  -perfect-dtlb\n")
  #f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l2-dcache\n")
  f.write("  -perfect-branch-pred\n")
  f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-base1.interval\n\n")

  ### base2 : l1 dcache + long lat###
  f.write("[run base2]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  f.write("  -perfect-l1-icache\n")
  f.write("  -perfect-l2-icache\n")
  f.write("  -perfect-dtlb\n")
  #f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l2-dcache\n")
  f.write("  -perfect-branch-pred\n")
  #f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-base2.interval\n\n")

  ### base3 : l1 cache + long lat + branch pred ###
  f.write("[run base3]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  f.write("  -perfect-l1-icache\n")
  f.write("  -perfect-l2-icache\n")
  f.write("  -perfect-dtlb\n")
  #f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l2-dcache\n")
  #f.write("  -perfect-branch-pred\n")
  #f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-base3.interval\n\n")

  ### sim1 : + l1 icache ###
  f.write("[run sim1]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  #f.write("  -perfect-l1-icache\n")
  f.write("  -perfect-l2-icache\n")
  f.write("  -perfect-dtlb\n")
  #f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l2-dcache\n")
  #f.write("  -perfect-branch-pred\n")
  #f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-sim1.interval\n\n")

  ### sim2 : + l2 icache ###
  f.write("[run sim2]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  #f.write("  -perfect-l1-icache\n")
  #f.write("  -perfect-l2-icache\n")
  f.write("  -perfect-dtlb\n")
  #f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l2-dcache\n")
  #f.write("  -perfect-branch-pred\n")
  #f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-sim2.interval\n\n")

  ### sim3 : + itlb ###
  f.write("[run sim3]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  #f.write("  -perfect-itlb\n")
  #f.write("  -perfect-l1-icache\n")
  #f.write("  -perfect-l2-icache\n")
  f.write("  -perfect-dtlb\n")
  #f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l2-dcache\n")
  #f.write("  -perfect-branch-pred\n")
  #f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-sim3.interval\n\n")

  ### sim4 : + l2 dcache ###
  f.write("[run sim4]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  #f.write("  -perfect-itlb\n")
  #f.write("  -perfect-l1-icache\n")
  #f.write("  -perfect-l2-icache\n")
  f.write("  -perfect-dtlb\n")
  #f.write("  -perfect-l1-dcache\n")
  #f.write("  -perfect-l2-dcache\n")
  #f.write("  -perfect-branch-pred\n")
  #f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-sim4.interval\n\n")

  ### inv1 : + l2 dcache ###
  f.write("[run inv1]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  f.write("  -perfect-l1-icache\n")
  f.write("  -perfect-l2-icache\n")
  f.write("  -perfect-dtlb\n")
  #f.write("  -perfect-l1-dcache\n")
  #f.write("  -perfect-l2-dcache\n")
  #f.write("  -perfect-branch-pred\n")
  #f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-inv1.interval\n\n")

  ### inv2 : + dtlb ###
  f.write("[run inv2]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
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
  f.write("  -interval "+interval_dir+"/%(bench)s-inv2.interval\n\n")

  ### inv3 : +  l1 icache ###
  f.write("[run inv3]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  #f.write("  -perfect-l1-icache\n")
  f.write("  -perfect-l2-icache\n")
  #f.write("  -perfect-dtlb\n")
  #f.write("  -perfect-l1-dcache\n")
  #f.write("  -perfect-l2-dcache\n")
  #f.write("  -perfect-branch-pred\n")
  #f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-inv3.interval\n\n")

  ### inv4 : +  l2 icache ###
  f.write("[run inv4]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-itlb\n")
  #f.write("  -perfect-l1-icache\n")
  #f.write("  -perfect-l2-icache\n")
  #f.write("  -perfect-dtlb\n")
  #f.write("  -perfect-l1-dcache\n")
  #f.write("  -perfect-l2-dcache\n")
  #f.write("  -perfect-branch-pred\n")
  #f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-inv4.interval\n\n")

  ### branch + dl1 ###
  f.write("[run perf-br-dl1]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-branch-pred\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-br-dl1.interval\n\n")

  ### branch + dl2 ###
  f.write("[run perf-br-dl2]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-l2-dcache\n")
  f.write("  -perfect-branch-pred\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-br-dl1.interval\n\n")

  ### branch + long lat ###
  f.write("[run perf-br-long]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-l2-dcache\n")
  f.write("  -perfect-long-lat\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-br-dl1.interval\n\n")

  ### perfect l1 cache ###
  f.write("[run perf-l1-cache]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-l1-dcache\n")
  f.write("  -perfect-l1-icache\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-perf-l1-cache.interval\n\n")

  ### perfect l2 cache ###
  f.write("[run perf-l2-cache]\n")
  f.write("suite = spec2006\n")
  #f.write("images = %(img_dir)s/spec2006.qcow2\n")
  f.write("images = %(img_dir)s/spec2006.qcow2."+fwd+"\n")
  #f.write("images = %(img_dir)s/spec2006_"+defn_new.disk[workload]+".qcow2\n")
  f.write("memory = 4096\n")
  f.write("simconfig = %(default_simconfig)s\n")
  f.write("  -logfile %(out_dir)s/%(bench)s.log\n")
  f.write("  -stats %(out_dir)s/%(bench)s.yml\n")
  f.write("  -machine single_core\n")
  f.write("  -perfect-l2-dcache\n")
  f.write("  -perfect-l2-icache\n")
  f.write("  -interval "+interval_dir+"/%(bench)s-perf-l2-cache.interval\n\n")
 
  f.close()

  return

### __main__ ###
try:
  insns = sys.argv[1]
  fwd = sys.argv[2]
  interval_dir = sys.argv[3]
  os.chdir('../')
  workloads = defn_new.get_workloads()
  for workload in workloads:
    make_cfgs(workload, insns, fwd, interval_dir)

except IndexError:
  print "Incorrect arguments..."
  print "Usage: ./make_cfgs.py [instructions(e.g. 100M)]"

