#!/bin/bash

# imputation pipeline

# Part 1: use bcftools to filter SNPs with following metrics:
#	 1. f_missing < 0.05
#	 2. single variants
#	 3. MAF > 0.005

# load bcftools and tabix
module load bcftools/1.9
module load tabix/0.2.6

# take argument from user input
VCF_file=$1
filtered=${VCF_file/.vcf.gz/.filtered.vcf.gz}
bcftools view -Oz -o $filtered \
	-i 'f_missing<0.05 && MAF[0]>0.005' \
	-m2 -M2 -v snp \
	$VCF_file
tabix -p vcf $filtered

# Part 2: use Eagle to phase the filtered file
phased=${filtered/.vcf.gz/.phased}
eagle --geneticMapFile $GENERIC_MAP \
	--outPrefix $phased \
	--numThreads 6 \
	--vcf $filtered \
	--vcfOutFormat z \
	--allowRefAltSwap
tabix -p vcf ${phased}.vcf.gz

# Part 3: split samples into reference and target

