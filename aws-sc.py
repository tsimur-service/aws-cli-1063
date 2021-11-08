import os
import json

#####################################
# 1) Output in table view ec2 insancec who has tag "Environment" = "Production"
os.system('aws ec2 describe-instances --filters Name=tag:Environment,Values=Production --output table --region '
          'eu-central-1')

#####################################
# 2) Take raw json and and ptocess it
raw_json_ec2 = os.popen('aws ec2 describe-instances --output json --region eu-central-1').read()

# file = open("tryam.txt")
# print(rawjson_ec2)

py_json_ec2 = json.loads(raw_json_ec2)

for vm_ec2 in py_json_ec2["Reservations"]:
    for tag in vm_ec2["Instances"][0]["Tags"]:
        if tag.get('Key') == 'Environment' and tag.get('Value') == 'Production':
            print("Instance ID: " + vm_ec2["Instances"][0].get('InstanceId'))
            print("Instance Name: " + next(item.get('Value') for item in vm_ec2["Instances"][0]["Tags"] if
                                           "Name" == item["Key"]))
            print("Elastic IP: " + vm_ec2["Instances"][0].get('PublicIpAddress'))
            print("SSH Keyname: " + vm_ec2["Instances"][0].get('KeyName'))
            print(" ")

#####################################
# 3)Output rds  instances so that maintance needed
os.system('aws rds describe-pending-maintenance-actions --output table')

#####################################
# 4) Output all the elastic Ip's that are not in use
os.system('aws ec2 describe-addresses --query "Addresses[?NetworkInterfaceId == null ].PublicIp"')

#####################################
# 5) Output all the SSL from ACM that are not in use

