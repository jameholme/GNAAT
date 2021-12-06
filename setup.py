# Setup.py
# By: James Holmes
# Installs required pip packages
# Creates files with required IDs and Keys for GNAAT.py

import subprocess
import sys

print("Installing required pip packages...")

subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "datetime"])

print("Please provide the following values...")

S3_Bucket = input("S3 Bucket Name: ")
with open("S3_Bucket", "w") as f:
    f.write(str(S3_Bucket))

AWS_ACL_ID = input("AWS ACL ID: ")
with open("AWS_ACL_ID", "w") as f:
    f.write(str(AWS_ACL_ID))

GN_API_Key = input("GreyNoise API Key: ")
with open("GN_API_Key", "w") as f:
    f.write(str(GN_API_Key))
