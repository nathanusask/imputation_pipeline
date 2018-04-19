#!/bin/bash

# this shell is to merge all the submerged 1500 VCF files into onw by chromosomes

prefix="Rice_1st_half"
for chr in chr{01..12}; do
	vcffiles=""
	for round in {1..25}; do
		file=${prefix}_${round}_${chr}.vcf.gz
		[[ ! -f $file.tbi ]] && tabix -p vcf $file &
		vcffiles="$vcffiles $file"
	done
	wait
	[[ ! -f ${prefix}_${chr}.vcf.gz ]] && ( bcftools merge -Oz -o ${prefix}_${chr}.vcf.gz $vcffiles; tabix -p vcf ${prefix}_${chr}.vcf.gz ) &
done
wait
