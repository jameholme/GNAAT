# GNAAT  
GreyNoise AWS ACL Tool (GNAAT) pronounced /ˈnæt/.  
GNAAT started out as a capstone project for school.  
It is a very simple tool that:  
1. Downloads VPC Flow Logs from a S3 Bucket
2. Checks the IPs against GreyNoise's IP classification tags
3. Creates AWS ACLs based on IPs tagged as Malicious
  
## Requirements:
* This tool requires you to run it form a Amazon Linux EC2 instance that has the required IAM Permissions that allows it to:
1. Download files from the S3 Bucket
2. Create ACL entries in the VPC

## Assumptions:
* This tool assumes your AWS ACL Rule 100 is the default allow-all rule that comes stock with most VPCs
  
## To-do:
* Start using Boto3 like a normal person
* If I can't manage to start using Boto3 like a normal person, start using Subprocess instead of OS.system???
* Maybe a setup file that takes in specific values required for this to work (VPC ID, ACL ID, S3 Bucket, GN API key, etc.)
* Make the Python not total garbage
