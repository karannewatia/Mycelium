# download SCALE-MAMBA
cd
git clone https://github.com/KULeuven-COSIC/SCALE-MAMBA.git

cd SCALE-MAMBA
git checkout -b v1.7 46a5fa4be

mv /root/config/CONFIG.mine .

mv /root/source/benchmark.sh .

# Use this if need to generate circuit for a new prime
mv /root/config/genSetupOption.sh
# Use this if using pre-generated circuit for existing prime
mv /root/config/runSetup.sh .
mv /root/config/genCertOptions.sh .
mv /root/config/genSecretSharingOptions.sh .

mv /root/config/IO.h ./src/Input_Output/
mv /root/config/Input_Output_File.cpp ./src/Input_Output/
mv /root/config/Input_Output_File.h ./src/Input_Output/
mv /root/config/Player.cpp ./src/

# WARNING: THIS PREVENTS YOU FROM USING GARBLED CIRCUITS
#  But if that's fine, this greatly improves efficiency.
mv /root/config/noabit.patch ./
git apply noabit.patch


make progs

# set up certificate authority
SUBJ="/CN=www.example.com"
cd Cert-Store

openssl genrsa -out RootCA.key 4096
openssl req -new -x509 -days 1826 -key RootCA.key \
           -subj $SUBJ -out RootCA.crt

# make 40 certificates. More can be added as necessary
mkdir csr
for ID in {0..39}
do
  SUBJ="/CN=player$ID@example.com"
  openssl genrsa -out Player$ID.key 2048
  openssl req -new -key Player$ID.key -subj $SUBJ -out csr/Player$ID.csr
  openssl x509 -req -days 1000 -set_serial 101$ID \
    -CA RootCA.crt -CAkey RootCA.key \
    -in csr/Player$ID.csr -out Player$ID.crt
done


prog_names=$(ls /root/source/ | grep mpc | sed 's/.mpc//')
# copy examples to correct locations
cd /root/SCALE-MAMBA
for EX in ${prog_names}
do
  mkdir Programs/$EX
  cp /root/source/$EX.mpc Programs/$EX/
  # If $EX does local computation, copy script for this. If not don't complain.
  cp /root/source/${EX}_local.py Programs/${EX}/local.py  2> /dev/null
  cp /root/source/${EX}_lib.py Programs/${EX}/${EX}_lib.py 2> /dev/null
done

# add simple syntax highlighting
cd
mkdir -p .vim/syntax
mv config/mamba.vim .vim/syntax
mkdir .vim/ftdetect
cd .vim/ftdetect
echo "au BufNewFile,BufRead *.wir set filetype=mamba" > mamba.vim
