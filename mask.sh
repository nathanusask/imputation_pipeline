#!/bin/bash

##first input is a gzipped file
mask_rt=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
for file in trial*/target.vcf.gz; do
	filename=$file

#begin to mask...
#note that the SNP region is in fields 10~9+samples
	for ratio in ${mask_rt[@]}; do
		./sub_mask.sh $filename $ratio &
	done
done
