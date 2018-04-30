#!/bin/bash

# this script utilizes mask.py to mask all target files under a directory by chromosome number
# chromosome number should be in format 'chr#', e.g., chr1

chrom=$1
for i in {1..10}; do
	for folder in ref_?_tgt_?_$chrom; do
		( prefix=${folder}/rep_$i
		tgt_file=${prefix}_tgt.vcf.gz
		tmp=${tgt_file##*/}
		./mask.py --filename $tgt_file --prefix ${tmp/.vcf.gz/}.mask --directory $folder
		) &
	done
	wait
done
wait
