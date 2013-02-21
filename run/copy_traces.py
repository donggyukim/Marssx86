#!/bin/env python

import os
import sys
import errno
import threading
import string

from time import gmtime, strftime

import defn

### __main__ ###
workloads = defn.get_workloads()

for workload in workloads:
  os.system("rsh itcb"+defn.itcb[workload]+" \"cd /tmp/vteori/results/"+workload+"_trace"+"; cp "+workload+".trace /data/forDonggyu/traces/"+"\"")
