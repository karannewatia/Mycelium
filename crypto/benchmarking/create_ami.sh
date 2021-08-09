# Creates a Linux 2 instance
# Must configure to use region us-east-1 (that is where that image is located.)
#aws ec2 run-instances --key-name ec2_0 --instance-type t2.xlarge --image-id ami-062f7200baf2fa504 --count 1
#aws ec2 run-instances --instance-type t2.xlarge --image-id ami-062f7200baf2fa504 --count 1


aws ec2 create-key-pair --key-name ec2
# save the private key in ~/Downloads/ec2.pem
aws ec2 run-instances --instance-type t2.xlarge --image-id ami-0d5eff06f840b45e9 --count 1


SRC_LOC=$1     # e.g. ec_elgamal
image_name=$2


DOCKER_NAME=docker0

# Assumes that ami is the ONLY running instance
ip=$(aws ec2 describe-instances --filters Name=instance-state-name,Values=running,pending | grep PublicIpAddress | grep -o \[0-9\.\]*)

instance_id=$(aws ec2 describe-instances --filters Name=instance-state-name,Values=running,pending | grep InstanceId | grep -o i-\[0-9a-f\]*)

#ssh_key="~/Downloads/AWScis.pem"
ssh_key="~/.ssh/ec2.pem"

# For some reason scp connection is being refused... maybe needs time to start up?
sleep 45

scp -i ${ssh_key} -o StrictHostKeyChecking=no -r ../code/scalemamba/${SRC_LOC} ec2-user@${ip}://home/ec2-user/${SRC_LOC}/ 

ssh -i ${ssh_key} -o StrictHostKeyChecking=no ec2-user@${ip} << EOF

sudo yum install -y docker

sudo service docker start

cd ${SRC_LOC}
sudo docker build -t ${DOCKER_NAME} .

EOF


image_id=$(aws ec2 create-image --instance-id ${instance_id} --name ${image_name} | grep -o ami\-\[a-f0-9\]*)
echo ${image_id}  >  ${image_name}.ami_id

# The above command takes a bit of time to complete. 
# If you try to terminate the instance while it is running, the above command fails
# Therefore, at some point after running this script, user must run ./terminate_all.sh
