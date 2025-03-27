# GNAAT
# By: James Holmes

import os
import datetime
import requests

# Read stored values from setup files
def read_value_from_file(filename):
    try:
        with open(filename, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run setup.py first.")
        exit(1)

# Load configuration values
acl_id = read_value_from_file("AWS_ACL_ID")
s3_bucket = read_value_from_file("S3_Bucket")
gn_api_key = read_value_from_file("GN_API_Key")

# Define the base directory
GNAAT_DIR = "/home/ec2-user/GNAAT/"
EXTRACTED_LOGS_DIR = os.path.join(GNAAT_DIR, "extracted-logs/")
GN_RESPONSES_DIR = os.path.join(GNAAT_DIR, "gn-responses/")
AWS_LOGS_DIR = os.path.join(GNAAT_DIR, "AWSLogs/")

# Ensure directories exist
os.makedirs(EXTRACTED_LOGS_DIR, exist_ok=True)
os.makedirs(GN_RESPONSES_DIR, exist_ok=True)
os.makedirs(AWS_LOGS_DIR, exist_ok=True)

# Download the S3 files into GNAAT directory
s3_download_cmd = f'aws s3 sync s3://{s3_bucket} {AWS_LOGS_DIR}'
os.system(s3_download_cmd)

# Extract the archives
yesterday = datetime.date.today() - datetime.timedelta(days=1)
date = yesterday.strftime('%Y/%m/%d/')

zip_directory = os.path.join(AWS_LOGS_DIR, '403614138459/vpcflowlogs/us-east-1/', date)
for path in os.listdir(zip_directory):
    full_zip_directory = os.path.join(zip_directory, path)

# Combines all of the downloaded archives for the day
combined_logs_path = os.path.join(EXTRACTED_LOGS_DIR, "logs.gz")
with open(combined_logs_path, 'ab') as logs:
    for f in full_zip_directory:
        with open(full_zip_directory, 'rb') as temp_logs:
            logs.write(temp_logs.read())

# Extracts the combined archives
unzip_cmd = f'gzip -d {combined_logs_path} -f'
os.system(unzip_cmd)

# Tidies up the log files
logs_path = os.path.join(EXTRACTED_LOGS_DIR, "logs")
unsorted_logs_path = os.path.join(EXTRACTED_LOGS_DIR, "unsorted_logs")
sorted_logs_path = os.path.join(EXTRACTED_LOGS_DIR, "sorted_logs")

tidy_cmd = f"cat {logs_path} | tr ' ' '\n' > {unsorted_logs_path} && sort -u {unsorted_logs_path} > {sorted_logs_path}"
os.system(tidy_cmd)

# Check GreyNoise for results
with open(sorted_logs_path) as ip_file:
    for ip in ip_file:
        ips = ip_file.readlines()
        ips = [ip.rstrip() for ip in ips]
        for ip in ips:
            headers = {
                "Accept": "application/json",
                "key": gn_api_key
            }
            url = f"https://api.greynoise.io/v3/community/{ip}"
            response = requests.request("GET", url, headers=headers)
            print(response.text)
            with open(os.path.join(GN_RESPONSES_DIR, ip), 'a') as r:
                r.write(response.text)

# Identify malicious IPs
bad_ips_path = os.path.join(EXTRACTED_LOGS_DIR, "bad_ips")
for file_name in os.listdir(GN_RESPONSES_DIR):
    full_path = os.path.join(GN_RESPONSES_DIR, file_name)
    with open(full_path) as f:
        if 'malicious' in f.read():
            with open(bad_ips_path, 'a') as bad_ip:
                bad_ip.write(file_name + '\n')

# Sort bad IPs
unsorted_bad_ips_path = os.path.join(EXTRACTED_LOGS_DIR, "unsorted_bad_ips")
sorted_bad_ips_path = os.path.join(EXTRACTED_LOGS_DIR, "sorted_bad_ips")

tidy_bad_ips_cmd = f"cat {bad_ips_path} | tr ' ' '\n' > {unsorted_bad_ips_path} && sort -u {unsorted_bad_ips_path} > {sorted_bad_ips_path}"
os.system(tidy_bad_ips_cmd)

# Use the Bad_IPs file to create ACLs in AWS to block traffic
date_rule = yesterday.strftime('%m%d')

# Create an Allow All at the highest rule number 32766
create_irule = f'aws ec2 create-network-acl-entry --network-acl-id {acl_id} --ingress --rule-number 32766 --protocol -1 --port-range From=0,To=65535 --cidr-block 0.0.0.0/0 --rule-action allow'
create_erule = f'aws ec2 create-network-acl-entry --network-acl-id {acl_id} --egress --rule-number 32766 --protocol -1 --port-range From=0,To=65535 --cidr-block 0.0.0.0/0 --rule-action allow'
os.system(create_irule)
os.system(create_erule)

# Delete the Allow All at rule number 100
delete_rule_i100 = f'aws ec2 delete-network-acl-entry --network-acl-id {acl_id} --ingress --rule-number 100'
delete_rule_e100 = f'aws ec2 delete-network-acl-entry --network-acl-id {acl_id} --egress --rule-number 100'
os.system(delete_rule_i100)
os.system(delete_rule_e100)

# Loop over IPs, create NACLs
with open(sorted_bad_ips_path) as f:
    rule_number = 0
    ips = f.readlines()
    ips = [ip.rstrip() for ip in ips]
    for ip in ips:
        rule_number += 1
        acl_cmd_ingress = f'aws ec2 create-network-acl-entry --network-acl-id {acl_id} --ingress --rule-number {date_rule}{rule_number} --protocol -1 --port-range From=0,To=65535 --cidr-block {ip}/32 --rule-action deny'
        print(acl_cmd_ingress)
        os.system(acl_cmd_ingress)
        acl_cmd_egress = f'aws ec2 create-network-acl-entry --network-acl-id {acl_id} --egress --rule-number {date_rule}{rule_number} --protocol -1 --port-range From=0,To=65535 --cidr-block {ip}/32 --rule-action deny'
        print(acl_cmd_egress)
        os.system(acl_cmd_egress)
