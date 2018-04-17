#!/bin/bash

originalVCF=$1; shift
chrom=$1
for folder in ref_?_tgt_?_$chrom; do
	for i in {1..10}; do
		prefix=${folder}/rep_${i}
		( bcftools view -Oz -o ${prefix}_ref.fmlt5.vcf.gz \
				-S ${prefix}_ref_samples.txt \
				-i 'f_missing<0.05' $originalVCF
		tabix -p vcf ${prefix}_ref.vcf.gz
		bcftools view -Oz -o ${prefix}_tgt.vcf.gz \
				-S ${prefix}_tgt_samples.txt \
				-R ${prefix}_ref.fmlt5.vcf.gz $originalVCF
		tabix -p vcf ${prefix}_tgt.vcf.gz ) &
	done
done

wait
