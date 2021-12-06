# GNAAT  
GreyNoise AWS ACL Tool (GNAAT) pronounced /ˈnæt/.  
GNAAT is a very simple tool that downloads VPC Flow Logs from an AWS S3 Bucket and checks the IPs within against GreyNoise's IP tags.  
GNAAT checks for malicious IPs and then creates AWS ACLs based on the findings.  
  
## To-do:
* Start using Boto3 like a normal person
* If I can't manage to start using Boto3 like a normal person, start using Subprocess instead of OS.system???
* Maybe a setup file that takes in specific values required for this to work (VPC ID, ACL ID, S3 Bucket, GN API key, etc.)
* Make the Python not total garbage
