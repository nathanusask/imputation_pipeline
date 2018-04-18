#!/bin/bash

# this script is to phase all the reference file using shapeit
# input is the chromosome number in 'chr#' format, e.g., chr1
# output will be in .shapeit.phased format

chrom=$1
for folder in ref_?_tgt_?_$chrom; do
	for i in {1..10}; do
		( prefix=${folder}/rep_$i
		ref_file=${prefix}_ref.fmlt5.vcf.gz
		shapeit -V $ref_file \
			-O ${ref_file/.vcf.gz/}.shapeit.phased \
			--force > ${ref_file/.vcf.gz/}.shapeit.phased.log
		shapeit -convert \
			--input-haps ${ref_file/.vcf.gz/}.shapeit.phased \
			--output-vcf ${ref_file/.vcf.gz/}.shapeit.phased.vcf
		bgzip -f ${ref_file/.vcf.gz/}.shapeit.phased.vcf
		tabix -p vcf ${ref_file/.vcf.gz/}.shapeit.phased.vcf.gz ) &
	done
done

