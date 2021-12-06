# GNAAT
# By: James Holmes

import os
import datetime
import requests
import datetime

# Modify these values with appropriate IDs
# The ID of the Network ACL that is associated with your monitored Subnets, can be the default NACL or a custom one
acl_id = 'acl-03ad6f29b150c5c52'

# The ID of the S3 Bucket where your VPC Flow Logs Reside
s3_bucket = 'capstone-vpcflowlogsbucket'

# Download the s3 files
s3_download_cmd = 'aws s3 sync s3://' + s3_bucket + ' .'
os.system(s3_download_cmd)

# Extract the archives
# Logs are saved by the day in S3 so the date is not hard-coded below
yesterday = datetime.date.today() - datetime.timedelta(days=1)
date = yesterday.strftime('%Y/%m/%d/')

zip_directory = '/home/ec2-user/capstone-project/AWSLogs/403614138459/vpcflowlogs/us-east-1/' + str(date)
for path in os.listdir(zip_directory):
    full_zip_directory = os.path.join(zip_directory, path)

# Combines all of the downloaded archives for the day
with open('/home/ec2-user/capstone-project/extracted-logs/logs.gz', 'ab') as logs:
    for f in full_zip_directory:
        with open(full_zip_directory, 'rb') as temp_logs:
            logs.write(temp_logs.read())

# Extracts the combined archives
combined_archives = '/home/ec2-user/capstone-project/extracted-logs/logs.gz'
unzip_cmd = 'gzip -d ' + str(combined_archives) + ' -f'
os.system(unzip_cmd)

# Tidies up the log files, placing each IP on its own row and then gets rid of the duplicates
tidy_cmd = "cat /home/ec2-user/capstone-project/extracted-logs/logs | tr ' ' '\n' > /home/ec2-user/capstone-project/extracted-logs/unsorted_logs && sort -u /home/ec2-user/capstone-project/extracted-logs/unsorted_logs > /home/ec2-user/capstone-project/extracted-logs/sorted_logs"
os.system(tidy_cmd)

# Iterates over the logs and checks Grey Noise for results
with open('/home/ec2-user/capstone-project/extracted-logs/sorted_logs') as ip_file:
    # Turns our file of IPs into a list
    for ip in ip_file:
        ips = ip_file.readlines()
        ips = [ip.rstrip() for ip in ips]
        # Sends the GET quests for the GN Results
        for ip in ips:
            headers = {
                "Accept": "application/json",
                # Update API Key as appropriate
                "key": "1"
            }
            url = "https://api.greynoise.io/v3/community/" + str(ip)
            response = requests.request("GET", url, headers=headers)
            print(response.text)
            # Saves the GN responses in their own file named after their IP
            with open('/home/ec2-user/capstone-project/gn-responses/' + ip, 'a') as r:
                r.write(response.text)

# Iterates over the GN Results searching for malicious IPs then writes them to a file
gn_responses = '/home/ec2-user/capstone-project/gn-responses/'
for file_name in os.listdir(gn_responses):
    full_path = os.path.join(gn_responses, file_name)
    with open(full_path) as f:
        if 'malicious' in f.read():
            with open('/home/ec2-user/capstone-project/extracted-logs/bad_ips', 'a') as bad_ip:
                bad_ip.write(file_name + '\n')

# Tidies up the Bad IPs file
tidy_bad_ips_cmd = "cat /home/ec2-user/capstone-project/extracted-logs/bad_ips | tr ' ' '\n' > /home/ec2-user/capstone-project/extracted-logs/unsorted_bad_ips && sort -u /home/ec2-user/capstone-project/extracted-logs/unsorted_bad_ips > /home/ec2-user/capstone-project/extracted-logs/sorted_bad_ips"
os.system(tidy_bad_ips_cmd)

# Use the Bad_IPs file to create ACLs in AWS to block all traffic
bad_ips = '/home/ec2-user/capstone-project/extracted-logs/sorted_bad_ips'
date_rule = yesterday.strftime('%m%d')

# Create an Allow All at the highest rule number 32766
create_irule = 'aws ec2 create-network-acl-entry --network-acl-id ' + acl_id + ' --ingress --rule-number 32766 --protocol -1 --port-range From=0,To=65535 --cidr-block 0.0.0.0/0 --rule-action allow'
create_erule = 'aws ec2 create-network-acl-entry --network-acl-id ' + acl_id + ' --egress --rule-number 32766 --protocol -1 --port-range From=0,To=65535 --cidr-block 0.0.0.0/0 --rule-action allow'
os.system(create_irule)
os.system(create_erule)
# Delete the Allow All at rule number 100
delete_rule_i100 = 'aws ec2 delete-network-acl-entry --network-acl-id ' + acl_id + ' --ingress --rule-number 100'
delete_rule_e100 = 'aws ec2 delete-network-acl-entry --network-acl-id ' + acl_id + ' --egress --rule-number 100'
os.system(delete_rule_i100)
os.system(delete_rule_e100)

# Loops over IPs, creates NACLs
with open(bad_ips) as f:
    for ip in bad_ips:
        rule_number = 0
        # Increments rule number and creates ingress rule
        ips = f.readlines()
        ips = [ip.rstrip() for ip in ips]
        for ip in ips:
            rule_number +=1
            acl_cmd_ingress = 'aws ec2 create-network-acl-entry --network-acl-id ' + acl_id + ' --ingress --rule-number ' + str(date_rule) + str(rule_number) + ' --protocol -1 --port-range From=0,To=65535 --cidr-block ' + ip + '/32 --rule-action deny'
            print(acl_cmd_ingress)
            os.system(acl_cmd_ingress)
            # Increments rule number and creates egress rule
            acl_cmd_egress = 'aws ec2 create-network-acl-entry --network-acl-id ' + acl_id + ' --egress --rule-number ' + str(date_rule) + str(rule_number) + ' --protocol -1 --port-range From=0,To=65535 --cidr-block ' + ip + '/32 --rule-action deny'
            print(acl_cmd_egress)
            os.system(acl_cmd_egress)
