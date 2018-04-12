#!/usr/bin/python

##this script is to mask vcf file according to certain ratio

import argparse
from math import floor, ceil
import random
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--ratio', type=float)
parser.add_argument('--samples', type=int)
parser.add_argument('--filename', type=str)
parser.add_argument('--output', type=str)
args = parser.parse_args()

ratio = args.ratio
samples = args.samples
import os
import sys
 
if sys.version.startswith("3"):
    import io
    io_method = io.BytesIO
else:
    import cStringIO
    io_method = cStringIO.StringIO

filename = args.filename
dirname = '/scratch/users/xuy962/trial1/'
fullnm = dirname + filename
p = subprocess.Popen(["zcat", fullnm], stdout=subprocess.PIPE)
fh = io_method(p.communicate()[0])
assert p.returncode == 0
output = args.output
file = open(output, 'w')
for line in fh:
	if '#' not in line and line:
		arr = line.rstrip('\n').split('\t')
		len_arr = len(arr)
		if len_arr <= 1:
			continue
		target = floor(samples*ratio)
		tarArr = []
		count = 0
	
		while count < target:
			tmp = random.randint(9, len_arr-1)
			if tmp not in tarArr:
				tarArr.append(tmp)
				count += 1
		for index in tarArr:
			if '|' in arr[index]:
				arr[index] = '.|.'
			else:
				arr[index] = '.'
		line = '\t'.join(arr)
		file.write(line+'\n')
	else:
		file.write(line)
file.close()

print 'Quiting python masking program...'
