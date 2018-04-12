#!/bin/bash

pid=$1
filename=$2

awk_ret=`top -b -p $pid -d 45 -n2 | awk -v pid=$pid -v OFS='\t' '$1~pid {print $6, $9, $10, $11}'`

while [[ ! -z $awk_ret ]]; do
	echo $awk_ret >> $filename
	awk_ret=`top -b -p $pid -d 45 -n2 | awk -v pid=$pid -v OFS='\t' '$1~pid {print $6, $9, $10, $11}'`
done
