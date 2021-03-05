Docker set up instructions:

docker build -t lwe .
docker run -it --rm lwe

in the docker:
apt-get install vim

use docker ps to get the id of the docker container running and then
copy the following from host to docker:
cp Downloads/SCALE-MAMBA-master/Auto-Test-Data/ 62eada770b41:/
cp Desktop/Cert-Store/ 62eada770b41:/root/SCALE-MAMBA/

in the docker:
cd ../..Auto-Test-Data
cp -r Cert-Store/ ~/SCALE-MAMBA/
cd ~/SCALE-MAMBA/
cp Auto-Test-Data/1/* Data/

To set up certs for N players:
bash ./genCertOptions.sh N 1 | ./Setup.x

Then set the mod with ./Setup.x -> 2 -> 2 -> mod
Then set up Conversion circuit if the prime is large

Test as follows:
./benchmark.sh lwe_test 0 1 2 ...
