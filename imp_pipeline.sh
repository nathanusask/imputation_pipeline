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
samples=sample_ids.txt
nSamples=$2
bcftools query -l $phased | tr '\t' '\n' | head -n $nSamples > $samples
for ref in {5..9}; do
	tgt=$(( 10-ref ))
	sub_folder=ref_${ref}_tgt_${tgt}
	[[ ! -d $sub_folder ]] && mkdir $sub_folder
	refSamples=$sub_folder/ref_samples.txt
	tgtSamples=$sub_folder/tgt_samples.txt
	i=0
	# split samples into ref and tgt sample files
	for samp in $(cat $samples); do
		( (( i%10<ref )) && echo $samp >> $refSamples ) || echo $samp >> $tgtSamples
		i=$(( i+1 ))
	done

	# use bcftools to split the phased VCF into ref and tgt VCF files
	refVCF=$sub_folder/reference.vcf.gz
	tgtVCF=$sub_folder/target.vcf.gz
	bcftools view -Oz -o $refVCF \
		-S $refSamples \
		$phased
	tabix -p vcf $refVCF
	bcftools view -Oz -o $tgtVCF \
		-S $tgtSamples \
		$phased
	tabix -p vcf $tgtVCF

	# Part 4: mask SNPs with specific missing rates
	# TODO: since each masking procedure takes a long time, consider parallelizing the tasks
	for mrate in {1..9}; do
		zcat $tgtVCF | while read line; do
			masked=${tgtVCF/.vcf.gz/}.0.$mrate.vcf.gz
			[[ -f $masked ]] && rm -f $masked
			( [[ `cut -c-1 <<< "$line"` == '#' ]] || (( RANDOM%10>=mrate )) ) && ( bgzip -c <<<"$line" >> $masked )
		done
	done
done

