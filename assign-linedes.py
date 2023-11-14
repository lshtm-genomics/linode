import argparse
import subprocess as sp
import json
import csv

parser = argparse.ArgumentParser(description='Assign line designations to a list of lines')
parser.add_argument('--infile', type=str, help='Input file',required = True)
parser.add_argument('--outfile', type=str, help='Output file',required = True)
args = parser.parse_args()

sp.run("linode-cli linodes  list --json > linodes.json", shell=True)

linodes = json.load(open("linodes.json", "r"))
# select only those with label starting with "user"
linodes = [l for l in linodes if l['label'].startswith('user')]
# sort by label
linodes = sorted(linodes, key=lambda k: k['label'], reverse=True)

participants = []
for row in csv.DictReader(open(args.infile,encoding='utf-8-sig')):
    participants.append(row)

# check there are enough linodes for each participant to have one
if len(participants) > len(linodes):
    print(f"Not enough linodes ({len(linodes)}) for each participant ({len(participants)}) to have one")
    exit()

for p in participants:
    l = linodes.pop()
    p['Linode'] = l['label']
    p['IP'] = l['ipv4'][0]

with open(args.outfile, 'w') as csvfile:
    fieldnames = list(participants[0])
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for p in participants:
        writer.writerow(p)