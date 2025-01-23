
# Bash wrapper to asg.py. 
# in theory, this could be part of asg.py, but I have split it out to show other skills.
#
# Usage: asg.sh
#
usage() { echo "i) interactive mode, c) cron mode" }

while getopts in ":i:c:*" options do
  case "$options" in

    i) read -p "Name of autoscaling group?" asg_name
       while [ "$done" != "N" ];
       do
          echo "Input data at prompts"
          read -p "EC2 Server Type:" type
          read -p "EC2 Server Number" number
          read -p "EC2 Server AMI" ami
          cat $type $number $ami >> asg_name
          read -p "Do you have another type to enter?" done
       done
       ;;
    c) read -p "Name of autoscaling group?" asg_name
       if [[ -f ]] asg_name;
       then
         #read "How often do you want check to run in minutes?" interval
         # get cron time here -- this requires some specification, since there are a huge
         # number of possible ranges.  By default, I've set it up to just accept the job
         # as running every minute.
         echo "* * * * * /path/to/asg.py $asg_name"
         #>> /path/to/cron/on/local/system/crontab
         else
         echo "Autoscaling group not found. Please run asg.sh with the -i flag to create an autoscaling group"
       fi
