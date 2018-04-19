#!/usr/bin/python

# this python file is to randomly generate 2 files -- one as reference and the other target
# input for this script is the chromosome number in a format such as 'chr1'
# for each different separate ratio, make 10 repliates

from sys import argv
import os
import errno

chrom = argv[1]

filename = 'samples.txt'
samples = []
with open(filename, 'r') as file:
	for line in file:
		samples.append(line.rstrip())
file.close()

import random
s_rate = [round(x/10.0, 1) for x in range(5,10)]
new_file_path_header = ['ref', '', 'tgt', '', chrom]
for rate in s_rate:
	ref = int(rate*10)
	tgt = int(10-ref)
	new_file_path_header[1] = str(ref)
	new_file_path_header[3] = str(tgt)
	new_file_path = '_'.join(new_file_path_header) + '/'
	if not os.path.exists(new_file_path):
		try:
			os.makedirs(new_file_path)
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise

	for rep in range(1,11):
		new_ref_filename = new_file_path + "rep_%d_ref_samples.txt"%(rep)
		new_tgt_filename = new_file_path + "rep_%d_tgt_samples.txt"%(rep)
		s_ref, s_tgt = [], []
		for sample in samples:
			rdm = random.uniform(0,1)
			if rdm > rate:
				s_tgt.append(sample)
			else:
				s_ref.append(sample)

		with open(new_ref_filename, 'w') as ref_file:
			ref_file.write('\n'.join(s_ref) + '\n')
		ref_file.close()
		with open(new_tgt_filename, 'w') as tgt_file:
			tgt_file.write('\n'.join(s_tgt) + '\n')
		tgt_file.close()

