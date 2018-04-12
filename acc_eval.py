#!/usr/bin/env python
'''
This python script is to calculate the imputation accuracy

The result file contains the following columns:
Chr: Chromosome number
Pos: position/locus
ID: SNP ID
MAF: minor allele frequency (of the reference panel)
AA-AA: correctly imputed homozygous dominant genotype
AA-AB: incorrectly impute homozygous dominant genotype to heterozygous
AA-BB: incorrectly impute homozygous dominant genotype to homozygous recessive
AB-AA
AB-AB
AB-BB
BB-AA
BB-AB
BB-BB


Note:
    for each imputed file, the original file to be compared to is always target.vcf.gz under the same directory
'''

from math import sqrt
from numpy import nanmedian, nanmean

# def calc_correlation(x_arr, y_arr):
#     assert len(x_arr) == len(y_arr)
#
#     sig_x, sig_y, sig_xy, sig_x_2, sig_y_2 = 0.0, 0.0, 0.0, 0.0, 0.0
#     for x, y in zip(x_arr, y_arr):
#         sig_x += x
#         sig_y += y
#         sig_xy += x*y
#         sig_x_2 += x*x
#         sig_y_2 += y*y
#
#     n = len(x_arr)
#     try:
#         r_ret = (n*sig_xy - sig_x*sig_y)/sqrt((n*sig_x_2 - sig_x*sig_x) * (n*sig_y_2 - sig_y*sig_y))
#         return r_ret
#     except:
#         return

def calc_concordance(x_arr, y_arr):
    assert len(x_arr) == len(y_arr)

    n_matches = sum([1 if x == y else 0 for x, y in zip(x_arr, y_arr)])

    return float(n_matches) / len(x_arr)

def calc_maf(str_info):
    str_arr = str_info.split(';')
    ac = 0
    an = 0
    for e in str_arr:
        if e.find('MAF') >= 0:
            return float(e.split('=')[1])

        if e.find('AF') >= 0:
            af = float(e.split('=')[1])
            return ( af if af < 0.5 else 1-af)

        if e.find('AC') >= 0:
            ac = int(e.split('=')[1])
        if e.find('AN') >= 0:
            an = int(e.split('=')[1])
    af = float(ac)/an
    return (af if af < 0.5 else 1 - af)

from scipy.stats import chisquare
from scipy.stats import pearsonr
def calc_stats(actual, imputed):
    dict_stats = {}
    dict_stats['imputed-MAF'] = calc_maf(imputed[7])

    gt_actual = [sum(list(map(int, x.split(':')[0].split('|')))) for x in actual[9:]]
    # gt_imputed = [sum(list(map(int, x.split(':')[0].split('|')))) for x in imputed[9:]]
    gt_imputed = [float(x.split(':')[1]) for x in imputed[9:]]
    # TODO: use chi-square to calculate the correlation between imputed and actual genotypes
    # dict_stats['correlation-rate'] = calc_correlation(gt_imputed, gt_actual)
    dict_stats['correlation-rate'] = pearsonr(gt_actual, gt_imputed)[0]
    dict_stats['concordance-rate'] = calc_concordance(gt_imputed, gt_actual)

    return dict_stats

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--missingRate", type=float)
parser.add_argument("--targetFile", type=str)
parser.add_argument("--imputeFileBgl", type=str)
parser.add_argument("--imputeFileMnmc", type=str)
args = parser.parse_args()

missing_rate = round(1 - args.missingRate, 2)
#here the missing rate is actually the percentage of unmasked genotypes
filename_targetFile = args.targetFile
filename_imputeFileBgl = args.imputeFileBgl
filename_imputeFileMnmc = args.imputeFileMnmc

headers = ['Chr', 'Pos', 'actual-MAF', 'MAF-Beagle', 'MAF-Minimac', 'Beagle Concordance rate',
           'Minimac Concordance rate', 'Beagle Correlation Rate', 'Minimac Correlation Rate']

import gzip

fp_target = gzip.open(filename_targetFile)
fp_bgl = gzip.open(filename_imputeFileBgl)
fp_mnmc = gzip.open(filename_imputeFileMnmc)

dirname = filename_targetFile.split('/')[0]
report_file_meta_filename = dirname + '/target.' + '%.2g'%(missing_rate) + '.accuracy.report.meta'
report_file_meta = open(report_file_meta_filename, 'w')
report_file_meta.write('\t'.join(headers) + '\n')

report_filename = report_file_meta_filename.rstrip('meta').rstrip('.')
report_file = open(report_filename, 'w')

actual_mafs = []
mnmc_imputed_mafs = []
bgl_imputed_mafs = []
bgl_concordance, bgl_correlation = [], []
mnmc_concordance, mnmc_correlation = [], []

#skip the meta information lines of the vcf files
curline_target = next(fp_target).decode('utf-8')
while curline_target[0] == '#':
    curline_target = next(fp_target).decode('utf-8')
curline_bgl = next(fp_bgl).decode('utf-8')
while curline_bgl[0] == '#':
    curline_bgl = next(fp_bgl).decode('utf-8')
curline_mnmc = next(fp_mnmc).decode('utf-8')
while curline_mnmc[0] == '#':
    curline_mnmc = next(fp_mnmc).decode('utf-8')

imputed_lines = 0
while True:
    #target_arr[7], i.e., the INFO column contains AC and AN
    target_arr = curline_target.rstrip('\n').split('\t')

    # genotype fields start from arr[9]
    bgl_arr = curline_bgl.rstrip('\n').split('\t')
    while bgl_arr[1] < target_arr[1]:
        curline_bgl = next(fp_bgl).decode('utf-8')
        bgl_arr = curline_bgl.rstrip('\n').split('\t')

    len_bgl_arr = len(bgl_arr)
    mnmc_arr = curline_mnmc.rstrip('\n').split('\t')
    while mnmc_arr[1] < target_arr[1]:
        curline_mnmc = next(fp_mnmc).decode('utf-8')
        mnmc_arr = curline_mnmc.rstrip('\n').split('\t')

    # For BEAGLE imputed file, IMP would appear in field#7
    # indicating that this line is imputed

    #on the other hand, 'GENOTYPED' would appear in filed#6 of minimac imputed file
    #indicating that this row is NOT imputed
    if bgl_arr[7].find('IMP') < 0 or mnmc_arr[6].find('GENOTYPED') >= 0:
        try:
            curline_target = next(fp_target).decode('utf-8')
        except:
            break
        try:
            curline_bgl = next(fp_bgl).decode('utf-8')
        except:
            break
        try:
            curline_mnmc = next(fp_mnmc).decode('utf-8')
        except:
            break
        continue

    actual_mafs.append(calc_maf(target_arr[7]))
    mnmc_stats = calc_stats(target_arr, mnmc_arr)
    bgl_stats = calc_stats(target_arr, bgl_arr)

    mnmc_imputed_mafs.append(mnmc_stats['imputed-MAF'])
    bgl_imputed_mafs.append(bgl_stats['imputed-MAF'])

    bgl_concordance.append(bgl_stats['concordance-rate'])
    bgl_correlation.append(bgl_stats['correlation-rate'])
    mnmc_concordance.append(mnmc_stats['concordance-rate'])
    mnmc_correlation.append(mnmc_stats['correlation-rate'])


    new_line = '\t'.join([ target_arr[0], target_arr[1],
                           '%.2g'%(actual_mafs[-1]), '%.2g'%(bgl_imputed_mafs[-1]), '%.2g'%(mnmc_imputed_mafs[-1]),
                           '%.2g'%(bgl_stats['concordance-rate']), '%.2g'%(mnmc_stats['concordance-rate']),
                           '%.2g'%(bgl_stats['correlation-rate']), '%.2g'%(mnmc_stats['correlation-rate'])
                           ]) + '\n'
    report_file_meta.write(new_line)

    imputed_lines += 1

    try:
        curline_target = next(fp_target).decode('utf-8')
    except:
        break
    try:
        curline_bgl = next(fp_bgl).decode('utf-8')
    except:
        break
    try:
        curline_mnmc = next(fp_mnmc).decode('utf-8')
    except:
        break


report_file_meta.close()
fp_bgl.close()
fp_mnmc.close()
fp_target.close()

#aggregate all the meta information from the above loop
r_maf_actual_bgl = pearsonr(actual_mafs, bgl_imputed_mafs)[0]
r_maf_actual_mnmc = pearsonr(actual_mafs, mnmc_imputed_mafs)[0]

hdr_summary = '#summary\t'
report_file.write(hdr_summary + 'Total lines imputed: ' + str(imputed_lines) + '\n')
report_file.write(hdr_summary + 'Correlation rate between acutal MAF and Beagle imputed MAF: %.2g\n' %(r_maf_actual_bgl))
report_file.write(hdr_summary + 'Correlation rate between acutal MAF and Minimac imputed MAF: %.2g\n\n' %(r_maf_actual_mnmc))
tmp_str = '#missing rate = ' + '%.2g'%(missing_rate)
report_file.write(tmp_str + '\n\n')

def get_bin_index(bins, maf):
    for idx, e in enumerate(bins):
        if maf < e:
            return (idx - 1)
    return len(bins) - 2


def binning(bins, mafs, x_arr):
    assert len(mafs) == len(x_arr)

    ret_bins = [[] for i in range(len(bins) - 1)]
    for maf, x in zip(mafs, x_arr):
        bin_idx = get_bin_index(bins, maf)
        ret_bins[bin_idx].append(x)
    return ret_bins

maf_bins = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.15, 0.25, 0.35, 0.5]
bgl_correlation_bins = binning(maf_bins, bgl_imputed_mafs, bgl_correlation)
bgl_concordance_bins = binning(maf_bins, bgl_imputed_mafs, bgl_concordance)
mnmc_correlation_bins = binning(maf_bins, mnmc_imputed_mafs, mnmc_correlation)
mnmc_concordance_bins = binning(maf_bins, mnmc_imputed_mafs, mnmc_concordance)


bgl_header = '#BGL\t'
generic_header = ['MAF-bins']
generic_measure1 = ['concordance', 'correlation']
generic_measure2 = ['min', 'max', 'median', 'average']
for i in generic_measure1:
    for j in generic_measure2:
        generic_header.append('-'.join([i, j]))
report_file.write(bgl_header + '\t'.join(generic_header) + '\n')
for i, (e_con_bin, e_cor_bin) in enumerate(zip(bgl_concordance_bins, bgl_correlation_bins)):
    tmp_list = ['%f--%f'%(maf_bins[i], maf_bins[i+1])]
    if len(e_con_bin) == 0:
        tmp_list += ['-' for j in range(4)]
    else:
        tmp_list += ['%.2g'%(min(bgl_concordance_bins[i])),
                    '%.2g'%(max(bgl_concordance_bins[i])),
                    '%.2g'%(nanmedian(bgl_concordance_bins[i])),
                    '%.2g'%(nanmean(bgl_concordance_bins[i]))]
    if len(e_cor_bin) == 0:
        tmp_list += ['-' for j in range(4)]
    else:
        tmp_list += ['%.2g'%(min(bgl_correlation_bins[i])),
                    '%.2g'%(max(bgl_correlation_bins[i])),
                    '%.2g'%(nanmedian(bgl_correlation_bins[i])),
                    '%.2g'%(nanmean(bgl_correlation_bins[i]))]
    report_file.write(bgl_header + '\t'.join(tmp_list) + '\n')

report_file.write('\n\n')

mnmc_header = '#MNMC\t'
report_file.write(mnmc_header + '\t'.join(generic_header) + '\n')
for i, (e_con_bin, e_cor_bin) in enumerate(zip(mnmc_concordance_bins, mnmc_correlation_bins)):
    tmp_list = ['%f--%f'%(maf_bins[i], maf_bins[i+1])]
    if len(e_con_bin) == 0:
        tmp_list += ['-' for j in range(4)]
    else:
        tmp_list += ['%.2g'%(min(mnmc_concordance_bins[i])),
                    '%.2g'%(max(mnmc_concordance_bins[i])),
                    '%.2g'%(nanmedian(mnmc_concordance_bins[i])),
                    '%.2g'%(nanmean(mnmc_concordance_bins[i]))]
    if len(e_cor_bin) == 0:
        tmp_list += ['-' for j in range(4)]
    else:
        tmp_list += ['%.2g'%(min(mnmc_correlation_bins[i])),
                    '%.2g'%(max(mnmc_correlation_bins[i])),
                    '%.2g'%(nanmedian(mnmc_correlation_bins[i])),
                    '%.2g'%(nanmean(mnmc_correlation_bins[i]))]

    report_file.write(mnmc_header + '\t'.join(tmp_list) + '\n')

report_file.write('\n\n')

report_file.close()
