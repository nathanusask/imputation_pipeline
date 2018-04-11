#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--infile', type=str)
parser.add_argument('--outfile', type=str)
args = parser.parse_args()

import gzip

filename = args.infile
cur_pos = 0
disregard_loci = []
with gzip.open(filename, 'r') as file:
#	wfile = open(args.outfile, 'w')
	for line in file:
		if line[0] == '#':
			continue
		arr_line = line.split('\t')[0:6]
		tmp_pos = arr_line[1]
		if tmp_pos == cur_pos and cur_pos not in disregard_loci:
			disregard_loci.append(tmp_pos)
			continue
		if (len(arr_line[3]) > 1 or len(arr_line[4]) > 1) and tmp_pos not in disregard_loci:
			disregard_loci.append(tmp_pos)
		cur_pos = tmp_pos
file.close()

print "Total number of disregarded loci: %d" %len(disregard_loci)

with gzip.open(filename, 'r') as file:
	wfile = gzip.open(args.outfile, 'w')
	for line in file:
		if line[0] == '#':
			wfile.write(line)
			continue
		tmp_pos = line.split('\t')[1]
		if tmp_pos in disregard_loci:
			continue
		wfile.write(line)
				
	wfile.close()
file.close()


