#!/bin/bash

#This script is to use demo_acc_eval.py to evaluate all the imputed files

target_file=target.vcf.gz
prefix=target.
bgl_postfix=.beagle.impute.vcf.gz
mnmc_postfix=.minimac3.impute.dose.vcf.gz
missing_rate=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
for dir in trial[56789]/; do
	for mrate in ${missing_rate[@]}; do
		cur_target_file=${dir}${target_file}
		cur_bgl_file=${dir}${prefix}${mrate}${bgl_postfix}
		cur_mnmc_file=${dir}${prefix}${mrate}${mnmc_postfix}
		./acc_eval.py --missingRate $mrate --targetFile $cur_target_file --imputeFileBgl $cur_bgl_file --imputeFileMnmc $cur_mnmc_file 1>/dev/null 2>/dev/null &
	done
done

wait