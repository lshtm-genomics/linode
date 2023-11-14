import argparse
import subprocess as sp
from uuid import uuid4
import csv
import plotly.express as px
from collections import defaultdict
import pandas as pd

argumentparser = argparse.ArgumentParser(description='Check progress of participants')
argumentparser.add_argument('--assigned-ips', type=str, help='Input file')

args = argumentparser.parse_args()

def get_progress(row):
    files = {
        'mapping': [
            '/home/user/data/tb/sample1.bam',
            '/home/user/data/tb/sample1.bam.bai',
            '/home/user/data/tb/sample2.bam',
            '/home/user/data/tb/sample2.bam.bai'
        ],
        "variants": [
            '/home/user/data/tb/variants/sample1.raw.vcf',
            '/home/user/data/tb/variants/sample2.raw.vcf',
            '/home/user/data/tb/variants/sample1.gatk.raw.vcf',
            '/home/user/data/tb/variants/sample2.gatk.raw.vcf',
            '/home/user/data/tb/variants/sample1.delly.vcf',
            '/home/user/data/tb/variants/sample2.delly.vcf',
        ],
        "assembly": [
            '/home/user/data/tb/sample1_asm/contigs.fasta',
            '/home/user/data/tb/sample1_asm/quast/report.txt',
            '/home/user/data/tb/sample1_asm/sample1_asm.crunch',
            '/home/user/data/tb/region.fastq',
            '/home/user/data/tb/region_assembly/contigs.fasta',
        ],
        "rnaseq": [
            '/home/user/data/transcriptomics/Mapping_Mtb/Mtb_L1.bam',
            '/home/user/data/transcriptomics/Mapping_Mtb/Mtb_L4.bam',
            '/home/user/data/transcriptomics/Mapping_Mtb/Mtb_L1_htseq_count.txt',
            '/home/user/data/transcriptomics/Mapping_Mtb/Mtb_L4_htseq_count.txt',
        ],
        "microbiome": [
            '/home/user/data/metagenomics/',
        ]
    }

    files_found = set()
    for l in sp.Popen('ssh root@%s "find /home/user/data -exec du -hs {} \;"' % row['IP'],stdout=sp.PIPE,shell=True).stdout:
        files_found.add(l.decode().strip().split('\t')[1])

    progress = {}
    for p in files:
        position = 1
        for f in files[p]:
            if f not in files_found:
                position = files[p].index(f)
                break
        file_coverage = len(set(files[p]).intersection(files_found)) / len(files[p])
        position = position/len(files[p])
        progress[p] = {'name':row['Full Name'],'IP':row['IP'],"complete_position":position,'coverage':file_coverage}
    return progress

results = defaultdict(list)
for row in csv.DictReader(open(args.assigned_ips,encoding='utf-8-sig')):
    progress = get_progress(row)
    print(row['Linode'],row['IP'],progress)
    for key in progress:
        results[key].append(progress[key])

df = pd.DataFrame(results['rnaseq'])
fig = px.histogram(df, x="coverage",nbins=100,template="simple_white",title="Progress of participants")
fig.write_html("progress.html")
fig.show()

print(df[df['coverage'] == 0])


