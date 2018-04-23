#!/bin/bash

##This bash script is to test Minimac3 imputation program
for folder in ref_?_tgt_?; do
	for i in {1..10}; do
		filePrefix=${folder}/rep_${i}
		ref_file=${filePrefix}_ref.fmlt5.shapeit.phased.vcf.gz
		tgt_file=${filePrefix}_tgt.vcf.gz
		Minimac3-omp --refHaps $ref_file --haps $tgt_file --prefix ${tgt_file/.vcf.gz/.minimac3.impute} --cpus 6 --log ON &
	done
done

wait
