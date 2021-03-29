Docker set up instructions:

Allocate at least 8 GB of memory for Docker

After starting the docker application:

inside MPC_lwe_elgamal-master:
cd/code/scalemamba/lwe
docker build -t lwe .    (this will take a while)
docker run -it --rm lwe

In another terminal inside MPC_lwe_elgamal-master:
use docker ps to get the id of the docker container running, and then
copy the following from host to docker:
docker cp Cert-Store/ id:/root/SCALE-MAMBA/
docker cp code/scalemamba/lwe/config/decrypt.sh id:/root/SCALE-MAMBA/Data/
docker cp code/scalemamba/lwe/config/key_gen.sh id:/root/SCALE-MAMBA/Data/

in the docker:
apt-get install vim    (for debugging)
cd ~/SCALE-MAMBA/
cp Auto-Test-Data/1/* Data/

To set up certs for N players:
bash ./genCertOptions.sh N 1 | ./Setup.x

Then set the mod with: ./Setup.x -> 2 -> 2 -> mod -> then enter the max possible t (threshold value)
Then set up Conversion circuit if the prime is large: ./Setup.x -> 3

Test as follows:
./benchmark.sh lwe_test 0 1 2 ...N-1

Output for Player i is in output_i.txt (or in Data/Playeri_out.txt)
Error message is in err_i.txt
Communication cost is in communication.txt


To benchmark key gen separately:

copy the following from host to docker:
docker cp code/scalemamba/lwe/inputs/key_gen_input.txt id:/
Note: key_gen_input.txt assumes polynomial degree = 2048 and lgP = 64. Generate a new key_gen_input.txt if the params are different

In the docker:
./Data/key_gen.sh N, where N is the number of players
Uncomment the key_gen section of lwe_test.mpc and comment out all other parts
If you edit the file on the host, then copy the file to the docker:
docker cp code/scalemamba/lwe/source/lwe_test.mpc id:/root/SCALE-MAMBA/Programs/lwe_test/lwe_test.mpc
./benchmark.sh lwe_test 0 1 2 ...N-1


To benchmark decrypt separately (do this after benchmarking key gen):

copy the following from host to docker:
docker cp code/scalemamba/lwe/inputs/decrypt_input.txt id:/
Note: decrypt_input.txt assumes polynomial degree = 2048. Generate a new decrypt_input.txt if the params are different

In the docker:
./Data/decrypt.sh N, where N is the number of players
Uncomment the decrypt section of lwe_test.mpc and comment out all other parts
If you edit the file on the host, then copy the file to the docker:
docker cp code/scalemamba/lwe/source/lwe_test.mpc id:/root/SCALE-MAMBA/Programs/lwe_test/lwe_test.mpc
./benchmark.sh lwe_test 0 1 2 ...N-1
