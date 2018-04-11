#!/bin/bash

for vcffile in ~/Rice/link{2..30}/*.vcf.gz; do
	tvcf=${vcffile##*/}
	tbifile=$vcffile.tbi
	[[ -f $tvcf || "$tvcf" == link*_chr*.vcf.gz ]] && rm -f $vcffile $tbifile || mv $vcffile $tbifile . &
done

wait

rm -f ~/Rice/link{2..30}/*.md5

