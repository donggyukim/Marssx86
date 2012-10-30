#!/bin/env python

import os
import sys
import errno
import threading

from time import gmtime, strftime

runs = {"400.perlbench":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"401.bzip2":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"403.gcc":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"410.bwaves":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"416.gamess":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"429.mcf":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"433.milc":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"435.gromacs":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"436.cactusADM":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"437.leslie3d":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"444.namd":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"445.gobmk":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"454.calculix":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"456.hmmer":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"458.sjeng":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"459.GemsFDTD":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"462.libquantum":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"464.h264ref":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"465.tonto":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"470.lbm":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"471.omnetpp":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"473.astar":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"481.wrf":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"482.sphinx3":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],"483.xalancbmk":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"]}



#runs = {"400.perlbench":["real-dl1"],"403.gcc":["real-dl1"]}

disk = {
    '400.perlbench':'1',
    '401.bzip2':'1',
    '403.gcc':'1',
    '410.bwaves':'1',
    '416.gamess':'5',
    '429.mcf':'1',
    '433.milc':'1',
    '435.gromacs':'2',
    '436.cactusADM':'2',
    '437.leslie3d':'2',
    '444.namd':'2',
    '445.gobmk':'2',
    '453.povray':'5',
    '454.calculix':'3',
    '456.hmmer':'3',
    '458.sjeng':'3',
    '459.GemsFDTD':'3',
    '462.libquantum':'4',
    '464.h264ref':'4',
    '470.lbm':'4',
    '471.omnetpp':'5',
    '473.astar':'4',
    '482.sphinx3':'5',
    '483.xalancbmk':'4'
    }

itcb = {
    '400.perlbench':'01',
    '401.bzip2':'01',
    '403.gcc':'02',
    '410.bwaves':'02',
    '416.gamess':'12',
    '429.mcf':'14',
    '433.milc':'14',
    '435.gromacs':'04',
    '436.cactusADM':'04',
    '437.leslie3d':'05',
    '444.namd':'05',
    '445.gobmk':'06',
    '453.povray':'12',
    '454.calculix':'07',
    '456.hmmer':'07',
    '458.sjeng':'08',
    '459.GemsFDTD':'08',
    '462.libquantum':'09',
    '464.h264ref':'09',
    '470.lbm':'10',
    '471.omnetpp':'13',
    '473.astar':'10',
    '482.sphinx3':'13',
    '483.xalancbmk':'11'
    }

class CFG :
  workload = ""
  cycles = ""
  warm_cycles = ""
  filename = ""

def get_time():
  return "["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"

def make_cfg(cfg):
  cfg.log.write(get_time()+" Setting config file.. \n")
  cfg.log.flush()
  filename = cfg.workload+"_"+cfg.target+"_"+cfg.cycles+"_"+cfg.warm_cycles+".cfg"
  f = open("util/"+filename,"w")
  f.write("[DEFAULT]\n")
  f.write("marss_dir = "+os.getcwd()+"\n")
  f.write("util_dir = %(marss_dir)s/utils\nimg_dir = /data/stall/qemu_disk\nqemu_bin = %(marss_dir)s/qemu/qemu-system-x86_64\n")
#  f.write("default_simconfig = -kill-after-run -quiet -run -stopuops "+cfg.cycles+" -anal-insns infinity -anal-uops "+cfg.warm_cycles+"\n\n")
  f.write("default_simconfig = -kill-after-run -quiet -run -stopinsns " + cfg.cycles + "\n")
  f.write("[suite spec2006-int]\n")
  f.write("checkpoints = "+cfg.workload+"\n\n")

  if(cfg.target == "perfect_branch"):
    f.write("[run perfect_branch]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/perfect_branch.log -stats %(out_dir)s/%(bench)s/perfect_branch.yml -machine single_core -perfect-branch-pred %(default_simconfig)s")

  if(cfg.target == "branch") :
    f.write("[run branch]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/branch.log -stats %(out_dir)s/%(bench)s/branch.yml -machine single_core %(default_simconfig)s -atrace %(out_dir)s/%(bench)s/branch.atrace -atrace2 %(out_dir)s/%(bench)s/branch.atrace2\n\n")

  if(cfg.target == "ID") :
    f.write("[run ID]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/ID.log -stats %(out_dir)s/%(bench)s/ID.yml -machine single_core %(default_simconfig)s -atrace-read %(out_dir)s/%(bench)s/branch.atrace -atrace-read2 %(out_dir)s/%(bench)s/branch.atrace2 -interval %(out_dir)s/%(bench)s/ID.interval -trace %(out_dir)s/%(bench)s/ID.trace\n\n")

  if(cfg.target == "perf") :
    f.write("[run perf]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/perf.log -stats %(out_dir)s/%(bench)s/perf.yml -machine single_core %(default_simconfig)s -atrace-read %(out_dir)s/%(bench)s/branch.atrace -atrace-read2 %(out_dir)s/%(bench)s/branch.atrace2 -interval %(out_dir)s/%(bench)s/perf.interval -trace %(out_dir)s/%(bench)s/perf.trace -perfect-il1 1 -perfect-itlb 1 -perfect-dl1 1 -perfect-dtlb 1 \n\n")

  if(cfg.target == "real-il1") :
    f.write("[run real-il1]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/real-il1.log -stats %(out_dir)s/%(bench)s/real-il1.yml -machine single_core %(default_simconfig)s -atrace-read %(out_dir)s/%(bench)s/branch.atrace -atrace-read2 %(out_dir)s/%(bench)s/branch.atrace2 -interval %(out_dir)s/%(bench)s/real-il1.interval -trace %(out_dir)s/%(bench)s/real-il1.trace -perfect-il2 1 -perfect-itlb 1 -perfect-dl1 1 -perfect-dtlb 1 \n\n")

  if(cfg.target == "real-dl1") :
    f.write("[run real-dl1]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/real-dl1.log -stats %(out_dir)s/%(bench)s/real-dl1.yml -machine single_core %(default_simconfig)s -atrace-read %(out_dir)s/%(bench)s/branch.atrace -atrace-read2 %(out_dir)s/%(bench)s/branch.atrace2 -interval %(out_dir)s/%(bench)s/real-dl1.interval -trace %(out_dir)s/%(bench)s/real-dl1.trace -perfect-il1 1 -perfect-itlb 1 -perfect-dl2 1 -perfect-dtlb 1 \n\n")

  if(cfg.target == "real-dl2") :
    f.write("[run real-dl2]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/real-dl2.log -stats %(out_dir)s/%(bench)s/real-dl2.yml -machine single_core %(default_simconfig)s -atrace-read %(out_dir)s/%(bench)s/branch.atrace -atrace-read2 %(out_dir)s/%(bench)s/branch.atrace2 -interval %(out_dir)s/%(bench)s/real-dl2.interval -trace %(out_dir)s/%(bench)s/real-dl2.trace -perfect-il1 1 -perfect-itlb 1 -perfect-dtlb 1 \n\n")

  if(cfg.target == "real-branch-dl2") :
    f.write("[run real-branch-dl2]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/real-branch-dl2.log -stats %(out_dir)s/%(bench)s/real-branch-dl2.yml -machine single_core %(default_simconfig)s -interval %(out_dir)s/%(bench)s/real-branch-dl2.interval -trace %(out_dir)s/%(bench)s/real-branch-dl2.trace -perfect-il1 1 -perfect-itlb 1 -perfect-dtlb 1 \n\n")

  if(cfg.target == "real-branch-dl1") :
    f.write("[run real-branch-dl1]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/real-branch-dl1.log -stats %(out_dir)s/%(bench)s/real-branch-dl1.yml -machine single_core %(default_simconfig)s -interval %(out_dir)s/%(bench)s/real-branch-dl1.interval -trace %(out_dir)s/%(bench)s/real-branch-dl1.trace -perfect-il1 1 -perfect-itlb 1 -perfect-dl2 1 -perfect-dtlb 1 \n\n")



  if(cfg.target == "IDB") :
    f.write("[run IDB]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/IDB.log -stats %(out_dir)s/%(bench)s/IDB.yml -machine single_core %(default_simconfig)s -interval %(out_dir)s/%(bench)s/IDB.interval -trace %(out_dir)s/%(bench)s/IDB.trace\n\n")
  if(cfg.target == "il1") :
    f.write("[run il1]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/il1.log -stats %(out_dir)s/%(bench)s/il1.yml -machine single_core %(default_simconfig)s -interval %(out_dir)s/%(bench)s/il1.interval -trace %(out_dir)s/%(bench)s/il1.trace -perfect-il1 1\n\n")
  if(cfg.target == "il2") :
    f.write("[run il2]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/il2.log -stats %(out_dir)s/%(bench)s/il2.yml -machine single_core %(default_simconfig)s -interval %(out_dir)s/%(bench)s/il2.interval -trace %(out_dir)s/%(bench)s/il2.trace -perfect-il2 1\n\n")
  if(cfg.target == "itlb") :
    f.write("[run itlb]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/itlb.log -stats %(out_dir)s/%(bench)s/itlb.yml -machine single_core %(default_simconfig)s -interval %(out_dir)s/%(bench)s/itlb.interval -trace %(out_dir)s/%(bench)s/itlb.trace -perfect-itlb 1\n\n")
  if(cfg.target == "dl1") :

    f.write("[run dl1]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/dl1.log -stats %(out_dir)s/%(bench)s/dl1.yml -machine single_core %(default_simconfig)s -interval %(out_dir)s/%(bench)s/dl1.interval -trace %(out_dir)s/%(bench)s/dl1.trace -perfect-dl1 1\n\n")
  if(cfg.target == "dl2") :

    f.write("[run dl2]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/dl2.log -stats %(out_dir)s/%(bench)s/dl2.yml -machine single_core %(default_simconfig)s -interval %(out_dir)s/%(bench)s/dl2.interval -trace %(out_dir)s/%(bench)s/dl2.trace -perfect-dl2 1\n\n")
  if(cfg.target == "dtlb") :
    f.write("[run dtlb]\nsuite = spec2006-int\nimages = %(img_dir)s/spec2006_"+disk[cfg.workload]+".qcow2\nmemory = 4096\n")
    f.write("simconfig = -logfile %(out_dir)s/%(bench)s/dtlb.log -stats %(out_dir)s/%(bench)s/dtlb.yml -machine single_core %(default_simconfig)s -interval %(out_dir)s/%(bench)s/dtlb.interval -trace %(out_dir)s/%(bench)s/dtlb.trace -perfect-dtlb 1\n\n")

  f.close()
  cfg.filename = filename
  cfg.log.write(get_time()+" Done!\n")
  cfg.log.flush()
  return

def run_cfg(cfg):
  cfg.log.write(get_time()+" Making Trace file.. \n")
  cfg.log.flush()
 
  command = ("util/run_bench.py -d /home/hanhwi/workspace/marss -c util/"+cfg.filename+" "+cfg.target+" 1>logs/"+cfg.workload+"/"+cfg.target+".out 2>logs/"+cfg.workload+"/"+cfg.target+".err")
#  print command
  os.system(command)
  cfg.log.write(get_time()+" Done!\n")
  cfg.log.flush()

def gzip_cfg(cfg):
  cfg.log.write(get_time()+" Compressing Trace file.. \n")
  cfg.log.flush()

  command = ("cd /work/dongju/"+cfg.workload+"/ ; gzip -c "+cfg.target+".trace > "+cfg.target+".trace.gz")
  os.system(command)
  cfg.log.write(get_time()+" Done!\n")
  cfg.log.flush()

class ThreadClass(threading.Thread):
  def __init__(self, workload, target):
    threading.Thread.__init__(self)
    self.workload = workload
    self.target = target

  def run(self):
    # step 1. Make Traces
    cfg = CFG()
    cfg.workload = self.workload
    cfg.target = self.target
    cfg.cycles = "100M"
    cfg.warm_cycles = "300M"

    log_dirpath = "logs/" + cfg.workload

    try:
      cfg.log = open(log_dirpath + "/" + cfg.target + ".log", "w")
    except IOError as e:
      if (e.errno == errno.ENOENT):
        os.makedirs(log_dirpath)
        cfg.log = open(log_dirpath + "/" + cfg.target + ".log", "w")
      else:
        raise
      
    make_cfg(cfg)
    run_cfg(cfg)

    # step 2. Gzip Traces
    # if(cfg.target != "branch"):
    #   gzip_cfg(cfg)

    # step 3. Run Analyzer
   
    cfg.log.close()

    # if(cfg.target == "branch"):
    #   th = ThreadClass(self.workload,"ID")
    #   th2 = ThreadClass(self.workload,"real-dl1")
    #   th3 = ThreadClass(self.workload,"perf")
       
    #   th.start()
    #   th2.start()
    #   th3.start()

    #   th.join()
    #   th2.join()
    #   th3.join()

    print (get_time()+"["+cfg.workload+"]["+cfg.target+"] All Done!")

t = ThreadClass(sys.argv[1], "perfect_branch")
t.start()
# for j in runs[sys.argv[1]]:
#   t = ThreadClass(sys.argv[1],j)
#   t.start()
