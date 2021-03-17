Docker set up instructions:

inside MPC_lwe_elgamal-master:
cd/code/scalemamba/lwe
docker build -t lwe .    (this will take a while)
docker run -it --rm lwe

in another terminal inside MPC_lwe_elgamal-master:
use docker ps to get the id of the docker container running, and then
copy the following from host to docker:
docker cp Cert-Store/ id:/root/SCALE-MAMBA/
docker cp code/scalemamba/lwe/config/player_copy.sh id:/root/SCALE-MAMBA/Data/  

in the docker:
apt-get install vim    (for debugging)
cd ~/SCALE-MAMBA/
cp Auto-Test-Data/1/* Data/

To set up certs for N players:
bash ./genCertOptions.sh N 1 | ./Setup.x

Then set the mod with ./Setup.x -> 2 -> 2 -> mod
Then set up Conversion circuit if the prime is large

Test as follows:
./benchmark.sh lwe_test 0 1 2 ...N-1
