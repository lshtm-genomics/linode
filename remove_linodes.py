import json
import subprocess as sp
import time 
from tqdm import tqdm

sp.run("linode-cli linodes  list --json > linodes.json", shell=True)

linodes = json.load(open("linodes.json", "r"))

for l in tqdm(linodes):
    time.sleep(2)
    sp.run(f"linode-cli linodes rm {l['id']}", shell=True)