#!/bin/bash

##This bash script is to test beagle imputation program

for folder in ref_?_tgt_?; do
	for i in {1..10}; do
		filePrefix=${folder}/rep_${i}
		vcf_ref_file=${filePrefix}_ref.fmlt5.shapeit.phased.vcf.gz
		vcf_tgt_file=${filePrefix}_tgt.vcf.gz
		( java -jar ${BEAGLE_PATH}/bref.08Jun17.d8b.jar $vcf_ref_file
		bref_file=${vcf_ref_file/.vcf.gz/.bref} 
		java -jar $BEAGLE_PATH/beagle.08Jun17.d8b.jar \
			gt=$vcf_tgt_file ref=$bref_file \
			out=${vcf_tgt_file/.vcf.gz/.beagle.impute} \
			nthread=6 ) &
	done
done

wait
