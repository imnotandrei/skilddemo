#
# bring in boto3
import boto3

#define shortnames and bring in environment variables
#region and account keys defined in local environment
ec2r = boto3.resource('ec2')
ec2c = boto3.client('ec2')
asg_dict = {}
# Get amount of instances per type

with open("asg.config") as asgconfig:
    for line in asgconfig:

        (key, val) = line.split()
        asg_dict[str(key)] = val

for instancetype, instancenumber in asg_dict.items():
    #This now becomes our main loop to check if we match what is required.

    print(instancetype, instancenumber)
    scale_info = ec2c.describe_instances(
        Filters=[
            {'Name': 'instance-type', 'Values': [instancetype]},
        ]
    )
    num_needed = int(instancenumber) - (len(scale_info) - 1)
    if num_needed > 0:
        ec2r.create_instances(InstanceType=[instancetype],MinCount=num_needed,MaxCount=num_needed)



#   print (num_needed)
#    print(scale_info)
#    print(len(scale_info) - 1)
# compare to instance numbers required
#
