import argparse
import subprocess as sp
import json
import time 
from tqdm import tqdm
parser = argparse.ArgumentParser(description='Assign line designations to a list of lines')
parser.add_argument('--total', type=int, help='Input file',required = True)

args = parser.parse_args()

sp.run("linode-cli linodes  list --json > linodes.json", shell=True)
linodes = json.load(open("linodes.json", "r"))
# select only those with label starting with "user"
linodes = [l for l in linodes if l['label'].startswith('user')]

labels = [l['label'] for l in linodes]
expected_labels = [f"user{i:02d}" for i in range(args.total)]

# check there are enough linodes for each participant to have one
tomake = [l for l in expected_labels if l not in labels]



# check there are enough linodes for each participant to have one
if len(tomake) > 0:
    for label in tqdm(tomake):
        # wait for 5 seconds to avoid rate limiting
        time.sleep(5)

        # label = "user" + str(i).zfill(2)
        cmd = "linode-cli linodes create --authorized_users jodyphelan --backups_enabled false --booted true --image 'linode/ubuntu20.04' --private_ip false --region eu-west --root_pass lshtmgenomics2023 --stackscript_data '{}' --stackscript_id 1095119 --type g6-standard-4" + f" --label {label}"
        sp.run(cmd, shell=True)
