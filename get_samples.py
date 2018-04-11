#!/usr/bin/python

filename = 'samples.txt'
samples = []
with open(filename, 'r') as file:
	for line in file:
		samples.append(line)
file.close()

from numpy import random
from math import floor
s_rate = [0.9, 0.8, 0.7, 0.6, 0.5]
new_file_path = 'trial'
new_filename_head = 'samples.'
new_filename_tail = '.txt'
total = len(samples)
for rate in s_rate:
	random.shuffle(samples)
	num1 = int(floor(total * rate))
	num2 = int(total - num1)
	samples1 = samples[0:num1]
	samples2 = [x for x in samples if x not in samples1]
	new_file_path = 'trial' + str(int(rate*10)) + '/'
	new_filename1 = new_file_path + new_filename_head + 'ref' + new_filename_tail
        new_filename2 = new_file_path + new_filename_head + 'target' + new_filename_tail
	with open(new_filename1, 'w') as file1:
		for sample in samples1:
			file1.write(sample)
	file1.close()
	with open(new_filename2, 'w') as file2:
		for sample in samples2:
			file2.write(sample)
	file2.close()

