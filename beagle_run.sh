#!/bin/bash

##This bash script is to test beagle imputation program

#if necessary, add script to make bref file of reference panel
#java -jar /grad/xuy962/Documents/beagle/bref.08Jun17.d8b.jar chr22.nodup.snp_only.vcf.gz
pids=""
for dir in trial*/; do
	java -jar /grad/xuy962/Documents/beagle/bref.08Jun17.d8b.jar ${dir}ref.vcf.gz &
	pids="$pids $!"
done
wait $pids

pids=""
for file in trial[5-9]/target.0.[1-9].vcf.gz; do
        bref_file=`dirname $file`/ref.bref
        #ref_file=`dirname $file`/samples.ref.vcf.gz
        echo "Imputing $file with reference file $reference using Beagle..."
        map_file=/scratch/users/xuy962/trial1/genetic.map/plink.chr22.GRCh37.map
        java -jar $BEAGLE_PATH/beagle.08Jun17.d8b.jar gt=$file ref=$bref_file impute=true map=$map_file out=${file/.vcf.gz/.beagle.impute} &
        bgl_pid=$!
        bgl_cpu_mem_file=${file/.vcf.gz/.beagle.impute}.cpu_mem.txt
        printf "MEM (default KiB)\tCPU (percentage)\tMEM (percentage)\tTime (since the beginning)\n" > $bgl_cpu_mem_file
        ./track_CPU_MEM.sh $bgl_pid $bgl_cpu_mem_file &
	pids="$pids $!"
done

wait $pids
