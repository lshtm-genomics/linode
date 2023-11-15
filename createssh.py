import argparse
import subprocess as sp
import csv

argumentparser = argparse.ArgumentParser(description='Set up SSH keys for participants')
argumentparser.add_argument('--assigned-ips', type=str, help='Input file with IP addresses', required=True)

args = argumentparser.parse_args()

def setup_ssh_keys(ip_address):
    try:
        command = f"ssh-copy-id user@{ip_address}"
        sp.run(command, shell=True, check=True)
    except sp.CalledProcessError as e:
        print(f"An error occurred while setting up SSH keys for IP: {ip_address}\nError: {e}")

def main():
    with open(args.assigned_ips, encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ip_address = row['IP']
            print(f"Setting up SSH keys for IP: {ip_address}")
            setup_ssh_keys(ip_address)

if __name__ == "__main__":
    main()