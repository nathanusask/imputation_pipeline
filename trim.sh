#!/bin/bash

##this file is to delete empty lines in the gzipped data file
pids=""
for file in *.0.[1-9].vcf; do
	tempfile=${file/.vcf/.new}
	tr -s '\n' <$file > $tempfile &
	pids="$pids $!"
done

wait $pids
pids=""
for file in *.0.[1-9].new; do
	tempfile=${file/.new/.vcf}
	rm -f $tempfile
	mv $file $tempfile
	bgzip -f $tempfile &
	pids="$pids $!"
done

wait $pids
./impute_run.sh 1> impute_run.log 2>impute_error.log &
