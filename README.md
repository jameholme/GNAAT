# GNAAT  
GreyNoise AWS ACL Tool (GNAAT) pronounced /ˈnæt/.  
GNAAT started out as a capstone project for school.  
It is a very simple tool that:  
1. Downloads VPC Flow Logs from a S3 Bucket
2. Checks the IPs against GreyNoise's IP classification tags
3. Creates AWS ACLs based on IPs tagged as Malicious
  
## To-do:
* Start using Boto3 like a normal person
* If I can't manage to start using Boto3 like a normal person, start using Subprocess instead of OS.system???
* Maybe a setup file that takes in specific values required for this to work (VPC ID, ACL ID, S3 Bucket, GN API key, etc.)
* Make the Python not total garbage
