local_path=$1
docker_path=$2   # e.g. SCALE-MAMBA/benchmark.sh
n_parties=$3

tmp_file=${RANDOM}.tmp
ip_addresses="./ip_addresses.txt"

for i in $(seq 1 ${n_parties} ); do 
    ip=$(cat ${ip_addresses} | sed "${i}q;d"); 
    scp -i ~/Downloads/AWScis.pem ${local_path} \
         ec2-user@${ip}://home/ec2-user/${tmp_file}; 
    container_id=$(ssh -i ~/Downloads/AWScis.pem ec2-user@${ip} sudo docker ps \
         | sed "2q;d" | grep -o ^\[0-9a-f\]*); 
    echo copying to container $container_id at $ip; 
    ssh -i ~/Downloads/AWScis.pem ec2-user@${ip} \
        sudo docker cp /home/ec2-user/${tmp_file} \
             ${container_id}://root/${docker_path}; 
    ssh -i ~/Downloads/AWScis.pem ec2-user@${ip} rm /home/ec2-user/${tmp_file}
done
