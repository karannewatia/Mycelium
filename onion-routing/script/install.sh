echo "install dependencies"
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install build-essential cmake autoconf automake libtool curl make unzip

echo "install g++ gcc 7.5.0"
sudo apt-get install gcc-7 g++-7
cd /usr/bin
sudo rm gcc
sudo ln -s gcc-7 gcc
sudo rm g++
sudo ln -s g++-7 g++

cd
echo "install opensll"
git clone https://github.com/openssl/openssl.git
cd openssl
git checkout c87a7f31a3db97376d764583ad5ee4a76db2cbef
./Configure
make
make test
sudo make install

# cd
# echo "remove older version openssl"
# sudo apt-get --purge remove openssl

cd
echo "install protobuf"
wget https://github.com/protocolbuffers/protobuf/releases/download/v3.14.0/protobuf-cpp-3.14.0.zip
unzip protobuf-cpp-3.14.0.zip
cd protobuf-3.14.0
./configure
make
make check
sudo make install
sudo ldconfig # refresh shared library cache.

wget https://cmake.org/files/v3.4/cmake-3.4.0-Linux-x86_64.tar.gz
tar -xzvf cmake-3.4.0-Linux-x86_64.tar.gz cmake-3.4.0-Linux-x86_64/
sudo mv cmake-3.4.0-Linux-x86_64 /opt/cmake-3.4.0
sudo ln -sf /opt/cmake-3.4.0/bin/*  /usr/bin/