#!/usr/bin/python

##This script is to make a file that contains 'old_sample_id new_sample_id\n' per line using samples.txt

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--old", type=str)
parser.add_argument("--new", type=str)
args = parser.parse_args()

old_filename = args.old
new_filename = args.new

read_file = open(old_filename, 'r')
write_file = open(new_filename, 'w')

for line in read_file:
	old_id = line.rstrip('\n')
	new_id = 'S_' + old_id
	write_file.write(new_id + '\n')

read_file.close()
write_file.close()

