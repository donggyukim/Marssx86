#!/bin/bash

for host in `cat ~/.available_hosts`
do
    pid_list=`rsh $host ps aux | grep $1 | grep -v grep | awk '{ print $2 }'`
    if [ -n "$pid_list" ]
    then
	rsh $host kill -9 $pid_list
    fi
done
