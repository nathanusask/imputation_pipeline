#!/bin/bash

##This bash script is to test Minimac3 imputation program
pids=""
for file in trial*/target.0.[1-9].vcf.gz; do
	ref_file=`dirname $file`/ref.vcf.gz
#	echo "Imputing $file with reference file $reference using Minimc3 ..."
	Minimac3 --refHaps $ref_file --haps $file --prefix ${file/.vcf.gz/.minimac3.impute} &
	mnmc_pid=$!
	mnmc_cpu_mem_file=${file/.vcf.gz/.minimac3.impute}.cpu_mem.txt
	printf "MEM (default KiB)\tCPU (percentage)\tMEM (percentage)\tTime (since the beginning)\n" > $mnmc_cpu_mem_file
        ./track_CPU_MEM.sh $mnmc_pid $mnmc_cpu_mem_file &
	pids="$pids $!"
done

wait $pids
