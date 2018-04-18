# imputation_pipeline

# Author: Nathan Yang
# Purpose: Master Thesis Project

#This project includes all the shell and python scripts used in my imputation pipeline

# sorted_Rice_download_links.txt contains all the FTP links of the 3000 individual Rice samples
# 1st_1500_samples.txt contains the FTP links for the first 1500 individual Rice samples
# 2nd_1500_samples.txt contains the FTP links for the second 1500 individual Rice samples

# ------------------- shell scripts ---------------------
# prep_1st_half.sh is the shell script used to download and merge the first 1500 individual samples
# prep_2nd_half.sh is the shell script used to download and merge the second 1500 individual samples

# mv_1st_half_vcf.sh was used to remove duplicate downloaded VCF files and bring all the unique VCF files together under the current directory
# merge_1st_half.sh: this shell is to merge all the sub-merged VCF files from the first 1500 samples into one by chromosomes

# check.sh checks if there are undownloaded VCF files and download the undownloaded VCF file(s) accordingly.

# phasing.sh: this shell is to phase reference VCF files with shapeit. the input is the chromosome number in format "chr#", e.g., chr1

# --------------------------------------------------------

# ------------------- python scripts ---------------------
# mask.py: to mask SNPs according to a randomly generated rate (0.0--1.0) at any genetic loci within a target dataset
#		three mandatory parameters: 	--filename sample.vcf.gz
#						--prefix output-prefix
#						--directory output-directory
#		two files will be generated after running this script:	.vcf		--masked VCF file
#									.mask.txt	--masking info file (this file should be used to simplify the accuracy evaluation process)
# get_samples.py: to randomly select samples to be put into either reference panel or target dataset. 
#		usage: one input is required: directory where the output files should be placed
#		output: five directories each with 20 txt files will be generated (10 reference samples txt files and 10 target samples txt files)

# --------------------------------------------------------
