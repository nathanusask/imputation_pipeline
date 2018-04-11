#!/bin/bash

#check.sh

# This is to check and download the individual VCF file that has not been downloaded

count=0
round=0
vcffiles=""
tbifiles=""
while read link1 link2 link3; do
	md5file=${link1##*/}
	[[ ! -f $md5file ]] && curl -o $md5file -s $link1

	vcffile=${link2##*/}
	if [[ ! -f $vcffile ]]; then
		curl -o $vcffile -s $link2 &
	else
		str1=$(grep "${vcffile}$" $md5file | tr -s ' ' | cut -d ' ' -f1)
		str2=$(md5sum $vcffile | tr -s ' ' | cut -d ' ' -f1)
		if [[ $str1 != $str2 ]]; then
			curl -o $vcffile -s $link2 &
		fi
	fi
	vcffiles="$vcffile $vcffiles"
	
	tbifile=${link3##*/}
	if [[ ! -f $tbifile ]]; then
		curl -o $tbifile -s $link3 &
	else
		str3=$(grep $tbifile $md5file | tr -s ' ' | cut -d ' ' -f1)
		str4=$(md5sum $tbifile | tr -s ' ' | cut -d ' ' -f1)
		if [[ $str3 != $str4 ]]; then
			curl -o $tbifile -s $link3 &
		fi
	fi
	tbifiles="$tbifile $tbifiles"

# 	echo "$link1\t$link2\t$link3" >> downloaded_links.txt
	
	(( count=count+1 ))
	[[ $count -lt '60' ]] && continue
	
	(( round=round+1 )) && wait
	
	[[ -f Rice_2nd_half_${round}_chr01.vcf.gz ]] && continue

	for file in $tbifiles; do
		touch $file
	done

	for chr in chr{01..12}; do 
		( bcftools merge -Oz -o Rice_2nd_half_${round}_${chr}.vcf.gz -r $chr $vcffiles; tabix -p vcf Rice_2nd_half_${round}_${chr}.vcf.gz ) &
	done
	
	vcffiles=""
	tbifiles=""
	count=0
	
	[[ $round -eq '25' ]] && break
done < 2nd_1500_samples.txt

wait

## when all the downloading processes are finished
## start merging them into a single VCF file
for chr in chr{01..12}; do
	( bcftools merge -Oz -o Rice_2nd_half_${chr}.vcf.gz Rice_2nd_half_{1..25}_${chr}.vcf.gz; tabix -p vcf Rice_2nd_half_${chr}.vcf.gz ) &
done

wait
