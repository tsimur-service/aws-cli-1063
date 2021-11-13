import os
import json
import re

# Specify custom parameters parametrs = ('<your aws-cli profile>', '<your aws region>'). Tuple used here to prevent
# accidentally changing data.
parametrs = ('ers', 'eu-west-2', 'default')
# os.system('aws ec2 describe-instances --output table --filters Name=tag:Environment,Values=Production' + '
# --profile ' + parametrs[0] + ' --region ' + parametrs[1])


#####################################
# 1) Output in table view ec2 instances who has tag "Environment" = "Production"
os.system('aws ec2 describe-instances --output table --filters Name=tag:Environment,Values=Production' + ' --profile ' + parametrs[0] + ' --region ' + parametrs[1])

####################################
# 2) Take raw json and and process it
raw_json_ec2 = os.popen('aws ec2 describe-instances --output json ' + ' --profile ' + parametrs[0] + ' --region '
                        + parametrs[1]).read()
py_json_ec2 = json.loads(raw_json_ec2)

elastic_ip_list = os.popen('aws ec2 describe-addresses --query "Addresses[].PublicIp" ' + ' --profile ' + parametrs[0]
                           + ' --region ' + parametrs[1]).read()
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

#####################################
# 3)Output rds  instances so that maintenance needed
os.system('aws rds describe-pending-maintenance-actions --output table ' + ' --profile ' + parametrs[0] + ' --region '
          + parametrs[1])

#####################################
# 4) Output all the elastic Ip's that are not in use
os.system('aws ec2 describe-addresses --query "Addresses[?NetworkInterfaceId == null ].PublicIp" ' + ' --profile '
          + parametrs[0] + ' --region ' + parametrs[1])

####################################
# 5) Output all the SSL from ACM that are not in use
raw_cert_list = os.popen('aws acm list-certificates ' + ' --profile ' + parametrs[0] + ' --region '
                         + parametrs[1]).read()
py_cert_list = json.loads(raw_cert_list)
cert_arns = [arn_item['CertificateArn'] for arn_item in py_cert_list['CertificateSummaryList']]

for arn in cert_arns:
    raw_json_cert = os.popen('aws acm describe-certificate --certificate-arn ' + arn + ' --profile ' + parametrs[0]
                             + ' --region ' + parametrs[1]).read()
    py_json_cert = json.loads(raw_json_cert)
    if len(py_json_cert['Certificate']['InUseBy']) == 0:
        print(py_json_cert['Certificate']['Serial'])
