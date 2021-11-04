import json

file = open("tryam.txt")
thisdict = json.load(file)

for vm_ec2 in thisdict["Reservations"]:
    for tag in vm_ec2["Instances"][0]["Tags"]:
        if tag.get('Key') == 'Environment' and tag.get('Value') == 'Production':
            print("Instance ID: " + vm_ec2["Instances"][0].get('InstanceId'))
            print("Instance Name: " + next(item.get('Value') for item in vm_ec2["Instances"][0]["Tags"] if item["Key"] == "Name"))
            print("Elastic IP: " + vm_ec2["Instances"][0].get('PublicIpAddress'))
            print("SSH Keyname: " + vm_ec2["Instances"][0].get('KeyName'))
            print(" ")

