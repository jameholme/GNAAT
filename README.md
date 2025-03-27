# GNAAT  
```
      _,---.  .-._         ,---.        ,---.   ,--.--------.  
  _.='.'-,  \/==/ \  .-._.--.'  \     .--.'  \ /==/,  -   , -\ 
 /==.'-     /|==|, \/ /, |==\-/\ \    \==\-/\ \\==\.-.  - ,-./ 
/==/ -   .-' |==|-  \|  |/==/-|_\ |   /==/-|_\ |`--`\==\- \    
|==|_   /_,-.|==| ,  | -|\==\,   - \  \==\,   - \    \==\_ \   
|==|  , \_.' )==| -   _ |/==/ -   ,|  /==/ -   ,|    |==|- |   
\==\-  ,    (|==|  /\ , /==/-  /\ - \/==/-  /\ - \   |==|, |   
 /==/ _  ,  //==/, | |- \==\ _.\=\.-'\==\ _.\=\.-'   /==/ -/   
 `--`------' `--`./  `--``--`         `--`           `--`--`   
```
GreyNoise AWS ACL Tool (GNAAT) pronounced /ˈnæt/.  
**It has no official affiliation with GreyNoise or AWS**, it just uses their stuff to do things.  
GNAAT started out as a project for school and will likely stay really bad.  
  
It is a *very* simple tool that:  
1. Downloads VPC Flow Logs from a S3 Bucket.
2. Checks the IPs against GreyNoise's IP classification tags.
3. Creates AWS ACLs based on IPs tagged as Malicious.
  
Q. *Is it really **that** useful to create ACLs in AWS???*  
A. Some would say no, that it's *"optional"*, but I say **yes**, because it adds an additional layer of security at the perimeter and I was bored.
  
Q. *Do we have to use GreyNoise???*  
A. If you're using this tool, yes, but even if you aren't, you should because GreyNoise is cool.
  
Q. *Doesn't GreyNoise already have really good integrations???*  
A. Yes... Please ignore this repository.
  
## Requirements:
* This tool requires you to run it from an EC2 instance or system that has the required AWS IAM Permissions that allows it to:
  - Download files from the S3 Bucket.
  - Create ACL entries in the VPC.
* This means you likely need to have ran AWS Configure at some point or another.

## Assumptions:
* This tool assumes your AWS ACL Rule 100 is the default allow-all rule that comes stock with most VPCs.
* It also assumes you have some VPC Flow Logs in a S3 Bucket somewhere.
  
## To-do List:
* Start using Boto3 like a normal person.
* If I can't manage to start using Boto3 like a normal person, start using Subprocess instead of OS.system???
