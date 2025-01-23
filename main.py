#
# bring in boto3
import boto3

#define shortnames and bring in environment variables
#region and account keys defined in local environment
ec2 = boto3.client('ec2')
asg_dict = {}
# Get amount of instances per type

with open("asg.config") as asgconfig:
    for line in asgconfig:
        (key, val) = line.split()
        asg_dict[int(key)] = val

for n,t in asg_dict():
    print (n,t)

scaletype = "t2.nano"

scale_info = ec2.describe_instances(
    Filters=[
        {'Name': 'instance-type', 'Values': [scaletype]},
    ]
)

print (scale_info)
print (len(scale_info)-1)
# compare to instance numbers required
#

