#!/bin/bash
#This bash script is to split the example.big.vcf into individuals

filename=chr22.vcf.gz
ratios=(9 7 5)
total=$(bcftools query -l $filename | wc -l)
echo "Total number of samples: $total"
sample_arr=()
for sample in `bcftools query -l $filename`; do
        sample_arr+=($sample)
done

each_time=10
for ratio in ${ratios[@]}; do
        fisrt_arr=()
        second_arr=()
        index=0
        while [ $index -lt $total ]; do
                count=0
                while true; do
                        if (( "$count" >= "$each_time" )) || (( "$index" >= "$total" )); then
                                break
                        fi

                        if [ $count -lt $ratio ]; then
                                first_arr+=(${sample_arr[$index]})
                        else
                                second_arr+=(${sample_arr[$index]})
                        fi
                        index=$(($index + 1))
                        count=$(($count + 1))
                done
        done

        list_file1=samples.${ratio}.1
        list_file2=samples.${ratio}.2
        for e in ${first_arr[@]}; do
                echo $e >> $list_file1
        done

        for e in ${second_arr[@]}; do
                echo $e >> $list_file2
        done

        bcftools view -c1 -Oz -S $list_file1 -o ${filename/.vcf*/.$ratio.1.vcf.gz} $filename --force-samples &
        bcftools view -c1 -Oz -S $list_file2 -o ${filename/.vcf*/.$ratio.2.vcf.gz} $filename --force-samples &

	unset first_arr
	unset second_arr
done

