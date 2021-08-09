n_players=$1
#threshold=$2
#program=$3
#n_io=$4
#local_in=$5
#local_out=$6
#plaintext_len=$7
#n_repeats=$8

#n_players, threshold: the same as for ./create_players.sh.
#program: the name of the particular test being run
#  (e.g. key generation and decryption should be different tests).
#n_io: the amount of input_ouput needed by each player.
#  If you don't know, put 0 (corresponds to infinity)
#  If there is no IO, put 1 (smallest value)
#local_in: true or false. Do players supply dynamic input to the protocol?
#local_out: true or false. Do players dynamically process output from protocol?
#
#prog_path=Programs/${program}
#echo $prog_path
#prog_path=$program
#
#ssh_key="~/Downloads/AWScis.pem"

docker_name=80d7d284596d

ssh_key="~/Downloads/myc.pem"
i=$n_players
#for i in $(seq 1 ${n_players}); do 
    player_i_ip=$(sed "${i}q;d" ip_addresses.txt)
    echo Connecting to player $i at $player_i_ip ...


    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo service docker start
    port_id=$(( 5000 + ${i} - 1))
    container_id=$(ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker run -id -p ${port_id}:${port_id} ${docker_name})


    #ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker ps | sed "2q;d"
    #container_id=$(ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker ps | sed "2q;d" | grep -o ^\[0-9a-f\]* )
    echo Connecting to container $container_id


    # Transfer all of the source files
    scp -i $ssh_key ../code/scalemamba/lwe/config/ConversionCircuit-LSSS_to_GC.txt ec2-user@${player_i_ip}:/home/ec2-user/
    ssh -i $ssh_key ec2-user@${player_i_ip} sudo docker cp //home/ec2-user/ConversionCircuit-LSSS_to_GC.txt ${container_id}://root/SCALE-MAMBA/Data/
    scp -i ${ssh_key} ../code/scalemamba/lwe/source/lwe_test.mpc ec2-user@${player_i_ip}://home/ec2-user/lwe_test.mpc
    scp -i ${ssh_key} ../code/scalemamba/lwe/source/key_gen.mpc ec2-user@${player_i_ip}://home/ec2-user/key_gen.mpc
    scp -i ${ssh_key} ../code/scalemamba/lwe/source/benchmark.sh ec2-user@${player_i_ip}://home/ec2-user/benchmark.sh
    scp -i ${ssh_key} ../code/scalemamba/lwe/config/decrypt.sh ec2-user@${player_i_ip}://home/ec2-user/decrypt.sh
    scp -i ${ssh_key} ../code/scalemamba/lwe/inputs/decrypt_input.txt ec2-user@${player_i_ip}://home/ec2-user/decrypt_input.txt

    #ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker cp //home/ec2-user/benchmark.sh ${container_id}://root/SCALE-MAMBA/benchmark.sh
    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker cp //home/ec2-user/decrypt.sh ${container_id}://root/SCALE-MAMBA/Data/decrypt.sh
    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker cp //home/ec2-user/decrypt_input.txt ${container_id}:/
    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker exec -i ${container_id} \
        bash -c '"cd SCALE-MAMBA; chmod 777 benchmark.sh; cd Data; chmod 777 decrypt.sh; cd ../; mkdir Programs; mkdir Programs/lwe_test; mkdir Programs/key_gen"' 
    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker cp //home/ec2-user/key_gen.mpc ${container_id}://root/SCALE-MAMBA/Programs/key_gen/key_gen.mpc
    ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker cp //home/ec2-user/lwe_test.mpc ${container_id}://root/SCALE-MAMBA/Programs/lwe_test/lwe_test.mpc


    #ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker exec -i ${container_id} bash -c '"cd SCALE-MAMBA; ./runSetup.sh '${n_players} ${threshold}'"'


    # COPY KEY_GEN OUTPUT INTO INPUT IF NEEDED
    #ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker exec -i ${container_id} \
    #    bash -c '"cd SCALE-MAMBA/Data; cp ../../../decrypt_input.txt Player${i}_in.txt"'
    #ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker exec -i ${container_id} \
    #    bash -c '"cd SCALE-MAMBA/Data; cp Players${i}_shareout.txt Player${i}_sharein.txt"'

    #ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker exec -i ${container_id} \
    #    bash -c '"cd SCALE-MAMBA; ./benchmark.sh '${program} ${n_players} ${threshold} ${n_io} ${local_in} ${local_out} ${plaintext_len} ${n_repeats} $((i - 1))' > output.txt"' &

#done
#
# 
#for i in $(seq 1 ${n_players}); do
#    wait
#done
#
#for i in $(seq 1 ${n_players}); do 
#    player_i_ip=$(sed "${i}q;d" ip_addresses.txt)
#    echo Connecting to player $i at $player_i_ip ...
#    container_id=$(ssh -i ${ssh_key} ec2-user@${player_i_ip} sudo docker ps \
#         | sed "2q;d" | grep -o ^\[0-9a-f\]* )
#    ssh -i ${ssh_key} ec2-user@${player_i_ip} \
#        sudo docker cp ${container_id}://root/SCALE-MAMBA/communication.txt /home/ec2-user/results_$(( $i - 1))_of_${n_players}.txt
#    scp -i ${ssh_key} ec2-user@${player_i_ip}://home/ec2-user/results_$(( $i - 1))_of_${n_players}.txt ./results_$(( $i - 1))_of_${n_players}.txt
#done
#
#
#sum=0
#for i in $(seq ${n_players}); do
#    comm=$(cat results_$( $i - 1 )_of_${n_players}.txt | grep "Communication Cost (bytes):" | grep -o [0-9]*)
#    sum=$(( ${sum} + ${comm} ))
#done
#
## Show the amortized cost
#ave=$(( ${sum} / ${n_players} / ${n_repeats} ))
#
#echo "Average Communication Cost (bytes):" ${ave} > results/${program}_${n_players}_lgm=${plaintext_len}_l=${n_repeats}.comm
#
#max=0
#for i in $(seq ${n_players}); do
#    time=$(cat results_$(( $i - 1 ))_of_${n_players}.txt | grep "Run time (s):" | grep -o [0-9]*)
#    # if (time > max) max = time
#    max=$(( (time > max)*time + (time <= max)*max ))
#done
#
## Show amortized time
#max=$(( max * 1000 / n_repeats ))
#
#echo "Run time (ms):" ${max} > results/${program}_${n_players}_lgm=${plaintext_len}_l=${n_repeats}.run_time
#
#rm results_*_of_${n_players}.txt
 
