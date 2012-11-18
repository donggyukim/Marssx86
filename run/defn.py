#!/bin/env python

import os
import sys
import errno
import threading

from time import gmtime, strftime

#runs = {
#	"400.perlbench":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"401.bzip2":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"403.gcc":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"410.bwaves":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"416.gamess":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"429.mcf":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"433.milc":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"435.gromacs":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"436.cactusADM":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"437.leslie3d":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"444.namd":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"445.gobmk":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"454.calculix":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"456.hmmer":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"458.sjeng":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"459.GemsFDTD":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"462.libquantum":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"464.h264ref":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"465.tonto":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"470.lbm":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"471.omnetpp":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"473.astar":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"481.wrf":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"482.sphinx3":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"],
#	"483.xalancbmk":["IDB","branch","il1","il2","itlb","dl1","dl2","dtlb","real-branch-dl2","real-branch-dl1"]}

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
    '400.perlbench':'14',
    '401.bzip2':'02',
    '403.gcc':'03',
    '410.bwaves':'04',
    '416.gamess':'05',
    '429.mcf':'06',
    '433.milc':'07',
    '435.gromacs':'08',
    '436.cactusADM':'09',
    '437.leslie3d':'10',
    '444.namd':'11',
    '445.gobmk':'12',
    '453.povray':'13',
    '454.calculix':'14',
    '456.hmmer':'13',
    '458.sjeng':'02',
    '459.GemsFDTD':'03',
    '462.libquantum':'04',
    '464.h264ref':'05',
    '470.lbm':'06',
    '471.omnetpp':'07',
    '473.astar':'08',
    '482.sphinx3':'09',
    '483.xalancbmk':'10'
    }

workloads = [
    ['400.perlbench',
    '401.bzip2',
    '403.gcc',
    '410.bwaves',
    '416.gamess',
    '429.mcf',
    '433.milc',
    '435.gromacs',
    '436.cactusADM',
    '437.leslie3d',
    '444.namd',
    '445.gobmk',
    '453.povray'],
    ['454.calculix',
    '456.hmmer',
    '458.sjeng',
    '459.GemsFDTD',
    '462.libquantum',
    '464.h264ref',
    '470.lbm',
    '471.omnetpp',
    '473.astar',
    '482.sphinx3',
    '483.xalancbmk']
    ]

def get_workloads():
  new_workloads = []
  [new_workloads.extend(group) for group in workloads]
  return new_workloads

configs = [
	"branch-pred", 
	"long-lat", 
	"itlb", 
	"l1-icache", 
	"l2-icache", 
	"dtlb", 
	"l1-dcache", 
	"l2-dcache"
	]

config0 = ["l1-icache", "l1-dcache"]
config1 = ["l1-icache", "l2-dcache"]
config2 = ["l1-icache", "long-lat"]
config3 = ["branch-pred", "l1-dcache"]
config4 = ["branch-pred", "l2-dcache"]
config5 = ["branch-pred", "long-lat"]
config5 = ["itlb", "l1-icache", "l2-icache"]
config6 = ["dtlb", "l1-dcache", "l2-dcache"]
config_combs = [
	config0,
	config1,
	config2,
	config3,
	config4,
	config5,
	config6,
	["branch-pred"] + config5,
	["branch-pred"] + config6,
	config5 + ["long-lat"],
	config6 + ["long-lat"],
	config5 + config6,
	["branch-pred"] + config5 + config6,
	config5 + config6 + ["long-lat"],
	configs
	]
