import os
import json
import re

# #####################################
# # 1) Output in table view ec2 instances who has tag "Environment" = "Production"
# os.system('aws ec2 describe-instances --filters Name=tag:Environment,Values=Production --output table --region '
#           'eu-central-1')

#####################################
# 2) Take raw json and and process it
raw_json_ec2 = os.popen('aws ec2 describe-instances --output json --region eu-central-1').read()
py_json_ec2 = json.loads(raw_json_ec2)

elastic_ip_list = os.popen('aws ec2 describe-addresses --query "Addresses[].PublicIp"').read()
elastic_ip_list = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", elastic_ip_list)

for vm_ec2 in py_json_ec2["Reservations"]:
    for tag in vm_ec2["Instances"][0]["Tags"]:
        if tag.get('Key') == 'Environment' and tag.get('Value') == 'Production' and vm_ec2["Instances"][0].get('PublicIpAddress') in elastic_ip_list:
            print("Instance ID: " + vm_ec2["Instances"][0].get('InstanceId'))
            print("Instance Name: " + next(item.get('Value') for item in vm_ec2["Instances"][0]["Tags"] if
                                           "Name" == item["Key"]))
            print("Elastic IP: " + vm_ec2["Instances"][0].get('PublicIpAddress'))
            print("SSH Keyname: " + vm_ec2["Instances"][0].get('KeyName'))
            print(" ")

# #####################################
# # 3)Output rds  instances so that maintenance needed
# os.system('aws rds describe-pending-maintenance-actions --output table')
#
# #####################################
# # 4) Output all the elastic Ip's that are not in use
# os.system('aws ec2 describe-addresses --query "Addresses[?NetworkInterfaceId == null ].PublicIp"')
#
# #####################################
# # 5) Output all the SSL from ACM that are not in use
