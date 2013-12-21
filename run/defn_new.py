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
    '400.perlbench':'02',
    '401.bzip2':'03',
    '403.gcc':'04',
    '429.mcf':'12',
    '445.gobmk':'13',
    '456.hmmer':'07',
    '458.sjeng':'08',
    '462.libquantum':'09',
    '464.h264ref':'10',
    '471.omnetpp':'11',
    '473.astar':'01',

    '483.xalancbmk':'01',
    '410.bwaves':'02',
    '416.gamess':'03',
    '433.milc':'04',
    '434.zeusmp':'12',
    '435.gromacs':'13',
    '436.cactusADM':'07',
    '437.leslie3d':'08',
    '444.namd':'09',
    '447.dealII':'10',

    '450.soplex':'02',
    '453.povray':'03',
    '454.calculix':'04',
    '459.GemsFDTD':'12',
    '465.tonto':'13',
    '470.lbm':'07',
    '481.wrf':'08',
    '482.sphinx3':'09',
    }

workloads = [
    ['400.perlbench',
    '401.bzip2',
    '403.gcc',
    '429.mcf',
    '445.gobmk',
    '456.hmmer',
    '458.sjeng',
    '462.libquantum',
    '464.h264ref',
    '471.omnetpp',
    '473.astar',],
    ['483.xalancbmk',
    '410.bwaves',
    '416.gamess',
    '433.milc',
    '434.zeusmp',
    '435.gromacs',
    '436.cactusADM',
    '437.leslie3d',
    '444.namd',
    '447.dealII',],
    ['450.soplex',
    '453.povray',
    '454.calculix',
    '459.GemsFDTD',
    '465.tonto',
    '470.lbm',
    '481.wrf',
    '482.sphinx3',],
   ]
 
"""
workloads = [
	['429.mcf',
    '445.gobmk',
    '454.calculix',
    '483.xalancbmk']
	]
"""

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
	"l2-dcache",
]

simple_configs = [
	"icache",
	"dcache",
	"frontend",
	"backend",
	"br-l1d",
	"br-l2d",
	#"br-dtlb",
	"br-long-lat",
	"br-backend",
	]

#config0 = ["l1-icache", "l1-dcache"]
#config1 = ["l1-icache", "l2-dcache"]
#config2 = ["l1-icache", "long-lat"]
#config3 = ["branch-pred", "l1-dcache"]
#config4 = ["branch-pred", "l2-dcache"]
#config5 = ["branch-pred", "long-lat"]
#config5 = ["itlb", "l1-icache", "l2-icache"]
#config6 = ["dtlb", "l1-dcache", "l2-dcache"]
#config_combs = [
#	config0,
#	config1,
#	config2,
#	config3,
#	config4,
#	config5,
#	config6,
#	["branch-pred"] + config5,
#	["branch-pred"] + config6,
#	config5 + ["long-lat"],
#	config6 + ["long-lat"],
#	config5 + config6,
#	["branch-pred"] + config5 + config6,
#	config5 + config6 + ["long-lat"],
#	configs
#	]

config_combs = [
	"base1",
	"base2",
	"base3",
	"sim1",
	"sim2",
	"sim3",
	"sim4",
	"inv1",
	"inv2",
	"inv3",
	"inv4",
]
