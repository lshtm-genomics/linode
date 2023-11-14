import json
import subprocess as sp
from uuid import uuid4
import csv
import argparse
from tqdm import tqdm 
import os

argparser = argparse.ArgumentParser(description='Check for conda environments on linodes')
argparser.add_argument('--outfile', type=str, help='Output file',required = True)
args = argparser.parse_args()

sp.run("linode-cli linodes  list --json > linodes.json", shell=True)

linodes = json.load(open("linodes.json", "r"))
# select only those with label starting with "user"
linodes = [l for l in linodes if l['label'].startswith('user')]
# reverse order of linodes so we can pop them off the end

required_envs = ['assembly', 'eqtl', 'gwas', 'mapping', 'methylation', 'microbiome', 'nanopore', 'phylogenetics', 'rnaseq', 'variant_detection']

rows = []
for l in tqdm(linodes):
    tmp = str(uuid4())
    ip = l['ipv4'][0]
    sp.run(f'ssh root@{ip} "/home/user/miniconda3/bin/conda env list" > {tmp}', shell=True)
    envs = []
    for line in open(tmp, "r"):
        row = line.strip().split()
        if "#" in line: continue
        if "base" in line: continue
        if line.strip()=='': continue
        if row[0] in required_envs:
            envs.append(row[0])
    rows.append({
        'Linode':l['label'], 
        'IP':ip,
        'Environments':len(envs),
        'Missing':','.join([e for e in required_envs if e not in envs])
    })
    os.remove(tmp)

with open(args.outfile, 'w') as csvfile:
    fieldnames = list(rows[0])
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(rows)