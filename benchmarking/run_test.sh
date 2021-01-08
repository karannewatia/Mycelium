n_players=$1
threshold=$2
program=$3
n_io=$4
local_in=$5
local_out=$6
plaintext_len=$7
n_repeats=$8

prog_path=Programs/${program}

ssh_key="~/Downloads/AWScis.pem"
for i in $(seq 1 ${n_players}); do 
    player_i_ip=$(sed "${i}q;d" ip_addresses.txt)
    echo Connecting to player $i at $player_i_ip ...
    container_id=$(ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker ps \
         | sed "2q;d" | grep -o ^\[0-9a-f\]* )
    echo Connecting to container $container_id
    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker exec -i ${container_id} \
        bash -c '"cd SCALE-MAMBA; ./benchmark.sh '${prog_path} ${n_players} ${threshold} ${n_io} ${local_in} ${local_out} ${plaintext_len} ${n_repeats} $((i - 1))' > output.txt"' &

done

 
for i in $(seq 1 ${n_players}); do
    wait
done

for i in $(seq 1 ${n_players}); do 
    player_i_ip=$(sed "${i}q;d" ip_addresses.txt)
    echo Connecting to player $i at $player_i_ip ...
    container_id=$(ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker ps \
         | sed "2q;d" | grep -o ^\[0-9a-f\]* )
    ssh -i ${ssh_key} ec2-user@${player_i_ip} \
        sudo docker cp ${container_id}://root/SCALE-MAMBA/communication.txt /home/ec2-user/results_$(( $i - 1))_of_${n_players}.txt
    scp -i ${ssh_key} ec2-user@${player_i_ip}://home/ec2-user/results_$(( $i - 1))_of_${n_players}.txt ./results_$(( $i - 1))_of_${n_players}.txt
done


sum=0
for i in $(seq ${n_players}); do
    comm=$(cat results_$(( $i - 1 ))_of_${n_players}.txt | grep "Communication Cost (bytes):" | grep -o [0-9]*)
    sum=$(( ${sum} + ${comm} ))
done

# Show the amortized cost
ave=$(( ${sum} / ${n_players} / ${n_repeats} ))

echo "Average Communication Cost (bytes):" ${ave} > results/${program}_${n_players}_lgm=${plaintext_len}_l=${n_repeats}.comm

max=0
for i in $(seq ${n_players}); do
    time=$(cat results_$(( $i - 1 ))_of_${n_players}.txt | grep "Run time (s):" | grep -o [0-9]*)
    # if (time > max) max = time
    max=$(( (time > max)*time + (time <= max)*max ))
done

# Show amortized time
max=$(( max * 1000 / n_repeats ))

echo "Run time (ms):" ${max} > results/${program}_${n_players}_lgm=${plaintext_len}_l=${n_repeats}.run_time

rm results_*_of_${n_players}.txt
 
