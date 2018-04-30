#!/usr/bin/python

# this script is to mask vcf file at any genetic loci
# there will be two output files
# one is the masked VCF file and the other a plain text file recording all the masked SNPs

import argparse
import random
import gzip

parser = argparse.ArgumentParser()
parser.add_argument('--filename', type=str)
parser.add_argument('--prefix', type=str)
parser.add_argument('--directory', type=str)
args = parser.parse_args()

dirname = args.directory if args.directory[-1] == '/' else args.directory + '/'
fullnm = args.filename
vcffile = gzip.open(fullnm, 'rb')

output_vcffilename = dirname + args.prefix + '.vcf.gz'
output_vcffile = gzip.open(output_vcffilename, 'wb')
output_mask_filename = dirname + args.prefix + '.txt.gz'
output_mask_file = gzip.open(output_mask_filename, 'wb')

header = ['pos', 'MAF', 'masking-rate',
          'missing-rate-before-masking', 'missing-rate-after-masking',
          'sample:GT-before-masking']

output_mask_file.write('\t'.join(header) + '\n')
for line_stream in vcffile:
    line = line_stream
    if line[0] == '#':
        output_vcffile.write(line)
        continue

    allele_count, allele_1_count = 0, 0
    arr = line.rstrip('\n').split('\t')
    arr_masked_snps, arr_s_gt = arr[:9], []
    masking_rate = random.uniform(0, 1)
    for idx, record in enumerate(arr[9:]):
        snp = record.split(':')[0]
        if snp.find('.') >= 0:
            arr_masked_snps.append(snp)
            continue
        char_split = snp[1]
        alleles = [int(x) for x in snp.split(char_split)]
        allele_count += 2
        allele_1_count += sum(alleles)
        rdm = random.uniform(0, 1)
        if rdm < masking_rate:
            arr_masked_snps.append('./.')
            arr_s_gt.append("%d:%s" % (idx, snp))
        else:
            arr_masked_snps.append(snp)

        pos = arr[1]
        af = float(allele_1_count) / allele_count
        maf = af if af < 0.5 else 1 - af
        n_samples = len(arr_masked_snps) - 9
        missing_rate_before_masking = 1 - float(allele_count / 2) / n_samples
        missing_rate_after_masking = 1 - float(allele_count / 2 - len(arr_s_gt)) / n_samples
        line_output_vcf = '\t'.join(arr_masked_snps)
        line_output_mask = '\t'.join([
            str(pos), str(maf), str(masking_rate),
            str(missing_rate_before_masking), str(missing_rate_after_masking),
            ';'.join(arr_s_gt)
        ])
    output_vcffile.write(line_output_vcf + '\n')
    output_mask_file.write(line_output_mask + '\n')

vcffile.close()
output_vcffile.close()
output_mask_file.close()

