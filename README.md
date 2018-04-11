# imputation_pipeline

#This project includes all the shell and python scripts used in my imputation pipeline

# sorted_Rice_download_links.txt contains all the FTP links of the 3000 individual Rice samples
# 1st_1500_samples.txt contains the FTP links for the first 1500 individual Rice samples
# 2nd_1500_samples.txt contains the FTP links for the second 1500 individual Rice samples

# prep_1st_half.sh is the shell script used to download and merge the first 1500 individual samples
# prep_2nd_half.sh is the shell script used to download and merge the second 1500 individual samples

# mv_1st_half_vcf.sh was used to remove duplicate downloaded VCF files and bring all the unique VCF files together under the current directory

# check.sh checks if there are undownloaded VCF files and download the undownloaded VCF file(s) accordingly.

