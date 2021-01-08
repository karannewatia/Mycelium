# install supporting mpir library
wget http://mpir.org/mpir-3.0.0.tar.bz2
tar -xvf mpir-3.0.0.tar.bz2
rm mpir-3.0.0.tar.bz2
cd mpir-3.0.0
./configure --enable-cxx
make install
cp .libs/* /usr/lib64/

# install openssl from source because apparently apt's version is not good
# enough
cd
wget https://www.openssl.org/source/openssl-1.1.1f.tar.gz
tar -xvf openssl-1.1.1f.tar.gz
rm openssl-1.1.1f.tar.gz
cd openssl-1.1.1f
./config
make
make install
ldconfig 
cd

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env 
