#!/bin/bash

# imputation pipeline

# Part 1: use bcftools to filter SNPs with following metrics:
#	 1. f_missing < 0.05
#	 2. single variants
#	 3. MAF > 0.005

# load bcftools
module load bcftools

# take argument from user input
VCF_file=$1
filtered=${VCF_file/.vcf.gz/.filtered.vcf.gz}
bcftools view -Oz -o $filtered \
	-i 'f_missing<0.05 && (TYPE="snp" && STRLEN(REF)=1 && STRLEN(ALT)=1) && MAF[0]>0.005' \
	$VCF_file

# Part 2: use Eagle to phase the filtered file
phased=${filtered/.vcf.gz/.phased}
eagle --geneticMapFile $GENERIC_MAP \
	--outputPrefix $phased \
	--numThreads 6 \
	--vcf $filtered \
	--vcfOutFormat z \
	--allowRefAltSwap

# Part 3: split samples into reference and target

