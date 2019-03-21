#!/bin/bash

# imputation pipeline

# part 1: use bcftools to filter SNPs with following metrics:
#	 1. f_missing < 0.05
#	 2. single variants
#	 3. MAF > 0.005

# load bcftools
module load bcftools

# take argument from user input
VCF_file=$1
bcftools view -Oz -o ${VCF_file/.vcf.gz/.filtered.vcf.gz} \
	-i 'f_missing<0.05 && TYPE="snp" && MAF[0]>0.005' \
	$VCF_file

