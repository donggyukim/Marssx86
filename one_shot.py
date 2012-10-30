#!/bin/env python

import os,sys
import threading
from time import gmtime, strftime

workloads = [["401.bzip2","400.perlbench","403.gcc","410.bwaves","416.gamess","429.mcf","433.milc"],["435.gromacs","436.cactusADM","437.leslie3d","444.namd","445.gobmk","454.calculix","456.hmmer"],["458.sjeng","459.GemsFDTD","462.libquantum","464.h264ref","470.lbm","473.astar","483.xalancbmk"]]

#workloads = [["400.perlbench","403.gcc"]]
#runs = {"400.perlbench":["perf"]}

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

def get_time():
  return "["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"

class ThreadClass(threading.Thread):
  def __init__(self, workload):
    threading.Thread.__init__(self)
    self.workload = workload
  def run(self):
    os.system("rsh itcb" + itcb[self.workload] + " \"cd " + os.getcwd() + "; ./one_shot_local.py "+ self.workload + "\"")

print (get_time()+" All Start!")

threads = []

for i in workloads[int(sys.argv[1])] :
  t = ThreadClass(i)
  t.start()
  threads.append(t)

for t in threads :
  t.join()

print (get_time()+" All Done!")
