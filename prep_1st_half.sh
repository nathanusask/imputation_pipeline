#!/bin/bash

#prep_1st_half.sh

# [[ -f downloaded_links.txt ]] && rm -f downloaded_links.txt

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
	
	for file in $tbifiles; do
		touch $file
	done
	for chr in chr{01..12}; do 
		bcftools merge -Oz -o Rice_1st_half_${round}_${chr}.vcf.gz -r $chr $vcffiles &
	done
	
	vcffiles=""
	tbifiles=""
	count=0
	
	[[ $round -eq '25' ]] && break

# 	(( count=count+1 ))
# 	[[ $count -lt '5' ]] && continue
# 	
# 	(( round=round+1 )) && wait
# 	
# 	for file in *.tbi; do
# 		touch $file
# 	done
# 	for chr in chr{01..12}; do 
# 		bcftools merge -Oz -o Rice_1st_half_${round}_${chr}.vcf.gz -r $chr $vcffiles &
# 	done
# 	
# 	vcffiles=""
# 	count=0
# 	
# 	[[ $round -eq '1' ]] && break
	
done < sorted_Rice_download_links.txt

wait
	
## when all the downloading processes are finished
## start merging them into a single VCF file
# for file in Rice_1st_half_{1..25}_${chr}.vcf.gz; do
# 	tabix -p vcf $file &
# done
# 
# wait
# 
# for chr in chr{01..12}; do 
# 	bcftools merge -Oz -o Rice_1st_half_${chr}.vcf.gz Rice_1st_half_{1..25}_${chr}.vcf.gz &
# 	#mergesplitpids="$! $mergesplitpids"
# done
# 
# wait

