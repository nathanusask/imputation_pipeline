#!/bin/bash

for file in trial*/ref; do
	bcftools view -c1 -Oz -S $file -o ${file}.vcf.gz chr22.nodup.snp_only.vcf.gz --force-samples &
done

for file in trial*/target; do
	bcftools view -c1 -Oz -S $file -o ${file}.vcf.gz chr22.nodup.snp_only.vcf.gz --force-samples &
done
