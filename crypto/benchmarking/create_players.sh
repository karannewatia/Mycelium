# Create multiple replicas according to the ami already created.
# This ami already has an image of a docker containing SCALE-MAMBA
n_players=$1
threshold=$2
image_name=$3

key_name=myc
docker_name=80d7d284596d

# Before doing anything else, terminate any existing instances.
# There should only be one type of instance running at a time
#./terminate_all.sh

# Seems that sometimes they stick around in the running state
#   from aws's perspective, even though I've asked them to terminate.
#   Therefore wait a bit so that they really terminate.
#sleep 10

# Assumes ami names begin with "ami"
ami_id=$(cat ${image_name}.ami_id)
# Using t2.small (2GB RAM) since t2.micro (1GB RAM) does not seem to have enough RAM
#aws ec2 run-instances --key-name ${key_name} --instance-type t2.small --image-id ${ami_id} --count ${n_players}
aws ec2 run-instances --key-name ${key_name} --instance-type t2.xlarge --image-id ${ami_id} --count ${n_players}

#rm ip_addresses.txt
aws ec2 describe-instances --filter Name=instance-state-name,Values=running,pending | grep PublicIpAddress | grep -o \[0-9\]\+\.\*\[0-9\]+ > ip_addresses.txt


# DO ALL PREVIOUS STUFF MANUALLY

rm NetworkData.txt

( echo RootCA.crt
echo ${n_players}
for i in $(seq 1 ${n_players}); do 
    echo $(( ${i} - 1)) $(sed "${i}q;d" ip_addresses.txt) \
    Player$(( ${i} - 1)).crt player$(( ${i} - 1))@example.com
done
echo 0
echo 0 ) > NetworkData.txt

echo NetworkData:
cat NetworkData.txt

# Wait for all instances to start running
while [ "$(aws ec2 describe-instances --filter Name=instance-state-name,Values=pending )" != "$(aws ec2 describe-instances --filter Name=instance-state-name,Values= )" ]; do echo 'instances pending...'; sleep 1; done

# I don't know why my ssh connections are being dropped... This seems to help.
#sleep 20

ssh_key="~/Downloads/${key_name}.pem"
for i in $(seq 1 ${n_players}); do
    player_i_ip=$(sed "${i}q;d" ip_addresses.txt)

    echo Adding ${player_i_ip} to list of known hosts...
    echo size before = $(stat ~/.ssh/known_hosts | grep -o Size..\[0-9\]* | grep -o \[0-9\]*)

    new_host=$( ssh-keyscan -H ${player_i_ip} )
    echo New Host: ${new_host}
    echo ${new_host} >> ~/.ssh/known_hosts
    sleep 3  # Again, not sure why the known_hosts file is not updating immediately...
    echo size after = $(stat ~/.ssh/known_hosts | grep -o Size..\[0-9\]* | grep -o \[0-9\]*)

    echo 'Copying file to ' ${player_i_ip}

    scp -i ${ssh_key} ./NetworkData.txt ec2-user@${player_i_ip}://home/ec2-user/NetworkData.txt
    scp -i ${ssh_key} ../code/scalemamba/lwe/config/genSecretSharingOptions.sh ec2-user@${player_i_ip}://home/ec2-user/genSecretSharingOptions.sh
    
    echo 'connecting by ssh to ' ${player_i_ip}

    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo service docker start
    port_id=$(( 5000 + ${i} - 1))
    #container_id=$(ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker run -id -p ${port_id}:${port_id} ${docker_name})
    container_id=$(ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker run -id -p ${port_id}:${port_id} ${docker_name})

    # This is dark magic... but it works. See comment by dr.doom at:
    #   https://stackoverflow.com/questions/3314660/passing-variables-in-remote-ssh-command
    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker cp ./genSecretSharingOptions.sh ${container_id}://root/SCALE-MAMBA/ 
    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker exec -i ${container_id} bash -c '"cd SCALE-MAMBA; ./runSetup.sh '${n_players} ${threshold}'"'
    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker exec -i ${container_id} bash -c '"curl --proto ’=https’ --tlsv1.2 -sSf https://sh.rustup.rs | sh"'
    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker cp ./NetworkData.txt ${container_id}:/root/SCALE-MAMBA/Data/

done 
  
