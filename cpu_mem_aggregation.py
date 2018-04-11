#!/usr/bin/env python

missing_rates = [round(x/10.0, 1) for x in range(1, 10)]
l_report_filename = ['target', '', '', 'impute.cpu_mem.txt']
l_str_program = ['beagle', 'minimac3']

# GB = 2**30
MB = 2**20
KB = 2**10

from numpy import mean

def aggregate_file(missing_rate, filename):
	dict_ret = {}
	
	l_time_elapsed = []
	l_mem = []
	l_cpu = []
	with open(filename, 'r') as fp:
		for line in fp:
			l_tmp = line.rstrip().split()
			str_mem = l_tmp[0]
			if str_mem[-1] == 'g':
				mem = round(float(str_mem.rstrip('g')), 2)
			elif str_mem[-1] == 'm':
				mem = round(float(str_mem.rstrip('m')) / KB, 2)
			else:
				mem = round(float(str_mem) / MB, 2)
			l_mem.append(mem)
			cpu = round(float(l_tmp[1]), 1)
			l_cpu.append(cpu)
			l_time = list(map(float, l_tmp[2].split(':')))
			time_elapsed = round(l_time[0] + l_time[1] / 60, 2)
			l_time_elapsed.append(time_elapsed)
	fp.close()
	time_elapsed = l_time_elapsed[-1]
	dict_ret['Total wall clock time'] = str(time_elapsed)
	# dict_ret['Average CPU consumption'] = str(round(sum(l_cpu) / time_elapsed, 2))
	dict_ret['Average CPU consumption'] = str(round(mean(l_cpu), 2))
	# tmp = sum(l_mem) / time_elapsed
	tmp = mean(l_mem)
	str_tmp = str(round(tmp, 1)) + 'G'
	if tmp < 1.0:
		tmp *= KB
		str_tmp = str(round(tmp, 1)) + 'M'
	if tmp < 1.0:
		tmp *=KB
		str_tmp = str(round(tmp, 1)) + 'K'
	dict_ret['Average Memory consumption'] = str_tmp
	dict_ret['Missing rate'] = str(round(1-missing_rate, 1))
	
	return dict_ret
	
generic_header = ['#program', 'missing rate', 'Mean CPU percentage', 'Mean memory usage', 'Wall clock time (min)']
for x in range(5,10):
	dirname = 'trial' + str(x) + '/'
	str_ratio = '##Reference:Target = %d:%d'%(x, 10-x)
	print(str_ratio)
	print('\t'.join(generic_header))
	for mrate in missing_rates:
		l_report_filename[1] = str(mrate)
		for str_program in l_str_program:
			l_report_filename[2] = str_program
			report_filename = dirname + '.'.join(l_report_filename)
			ret = aggregate_file(mrate, report_filename)
			lineToPrint = '\t'.join(['#%s'%str_program,
										ret['Missing rate'],
										ret['Average CPU consumption'],
										ret['Average Memory consumption'],
										ret['Total wall clock time']
										])
			print(lineToPrint)
	print('\n\n')
	
