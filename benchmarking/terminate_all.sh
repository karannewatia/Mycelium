
instance_ids=$( aws ec2 describe-instances | grep InstanceId | grep -o i-\[0-9a-f\]* | tr '\n' ' ' )
aws ec2 terminate-instances --instance-ids ${instance_ids}

rm ./ip_addresses.txt
rm ./NetworkData.txt
