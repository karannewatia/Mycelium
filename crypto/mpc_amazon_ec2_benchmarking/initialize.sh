image_name=ami_myc

key_name=myc
docker_name=80d7d284596d

ami_id=$(cat ${image_name}.ami_id)

aws ec2 run-instances --key-name ${key_name} --instance-type t2.xlarge --image-id ${ami_id} 

#rm ip_addresses.txt
aws ec2 describe-instances --filter Name=instance-state-name,Values=running,pending | grep PublicIpAddress

# Now copy into the file and run run_test.sh

