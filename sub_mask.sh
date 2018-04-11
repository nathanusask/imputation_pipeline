#!/bin/bash

##[HELP] 
#$1 = filename
#$2 = mask ratio
#
##first input is a gzipped file
echo "begin the bash script..."
date

echo "Starting masking program..."
date
pids=""
filename=$1
ratio=$2

#begin to mask...
#note that the SNP region is in fields 10~9+samples
new_file=${filename/.vcf.gz/.${ratio}.vcf.gz}
echo "Generating $new_file ..."
zcat $filename | awk -v ratio=$ratio '$1~/^#/ || rand() >= ratio' > ${new_file/.gz/}
bgzip -f ${new_file/.gz/}
tabix -f -p vcf $new_file
echo "Masking script finished."
date
