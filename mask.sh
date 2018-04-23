#!/bin/bash

# this script utilizes mask.py to mask all target files under a directory by chromosome number
# chromosome number should be in format 'chr#', e.g., chr1

chrom=$1
for folder in ref_?_tgt_?_$chrom; do
	for i in {1..10}; do
		( prefix=${folder}/rep_$i
		tgt_file=${prefix}_tgt.vcf.gz
		tmp=${tgt_file##*/}
		./mask.py --filename $tgt_file --prefix ${tmp/.vcf.gz/}.mask --directory $folder
		vcf_masked=${tmp/.vcf.gz/}.mask.vcf
		bgzip -f ${tmp/.vcf.gz/}.mask.vcf
		tabix -p vcf ${tmp/.vcf.gz/}.mask.vcf.gz
		gzip ${tmp/.vcf.gz/}.mask.txt ) &
	done
done

wait
