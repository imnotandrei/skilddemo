# This is a very basic autoscaler, designed to maintain a minimum level of an enviroment across
# multiple machine types.
#
# Areas for improvement going forward would be
#
# 1) to include a removal method, as described below,
# 2) the ability to specify ami according to instance type; the latter would be done via a file
# with the following format:
#
# <instancetype> <instancenumber> <instancetype_ami>
#
# 3) Permit multiple amis per isntance type by adding a "group" classification to the input file
# so that the file would read:
# <group> <instancetype> <instancenumber> <instancetype_ami>
#
# However, I think at this point we're getting closer to reimplementing terraform, instead of
# reimplementing an ASG.
#
# Usage: asg.py <autoscaling group file> -- this could be run in, say, cron at whatever interval
# seems appropriate.
#
# Note: 2) completed by turning the input into a dict with a list value for each key.
#

# bring in boto3

import boto3

#define shortnames and bring in environment variables
#region and account keys defined in local environment
ec2r = boto3.resource('ec2')
ec2c = boto3.client('ec2')
asg_dict = {}
# Get amount of instances per type

# This is set to open a specified file due to the limitations of my development environment
# and time; I have added a commented-out line to show what would be the correct in-operation use.,
# This presumes a different file for each ASG, as written in the BASH wrapper.

with open("asg.config") as asgconfig:
# with open(sys.argv[1]) as asgconfig:
    for line in asgconfig:

        (key, val1, val2) = line.split(":")
        asg_dict[str(key)] = [val1, val2]

# print (asg_dict)

for instancetype, instancedata in asg_dict.items():
    #This now becomes our main loop to check if we match what is required.
#   print(type(instancetype))
#   print(instancetype, instancenumber)
#   moved the next two lines to the top of the loop for clarity's sake.

    instancenumber = (instancedata[0])
    instanceami = instancedata[1].strip()

#

    scale_info = ec2c.describe_instances(
        Filters=[
            {'Name': 'instance-type', 'Values': [instancetype]},
        ]
    )
# Note: This only works to maintain a level of instances -- it will not scale down at the moment.
# num_needed could be used to reduce, with a loop pulling up the first instance-id and deleting it,
# looping over num_needed times -- this presumes all instances are identical.

    num_needed = int(instancenumber) - (len(scale_info) - 1)
    if num_needed > 0:
        ec2r.create_instances(ImageId=instanceami,InstanceType=instancetype,MinCount=num_needed,MaxCount=num_needed)

# print statements are commented out but left in to show debugging process.
#

#   print (num_needed)
#    print(scale_info)
#    print(len(scale_info) - 1)
# compare to instance numbers required
#
