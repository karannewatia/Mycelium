### Rough instructions to run on EC2 with 10 machines:

- Create 10 xlarge instances. Make sure to configure your security settings to allow incoming traffic on at least ports 5000-5000+N-1, where N is the number of machines

- SSH into each instance. On each node, do the following:

`sudo yum install docker`
`sudo yum install git`

`sudo service docker start`

`git clone https://github.com/karannewatia/Mycelium.git`

`cd Mycelium/crypto/code/scale_mamba_version`

`sudo docker build -t mpc . `

Set bash variables i=1 to i=10 for each corresponding node

`port_id=$(( 5000 + ${i} - 1))`

`sudo docker run -id -p ${port_id}:${port_id} mpc `

(This will work even if you close the docker and need  to run it again:
`sudo docker ps`
Grab the ID and run `sudo docker exec -ti [ID] bash`)

`cd SCALE-MAMBA`

`curl ifconfig.me` and store the resulting IP address

In this folder, create a cert.sh file as follows, with the IP addresses filled in:

`echo 1
echo RootCA
echo 10
echo IP0
echo Player0.crt
echo IP1
echo Player1.crt
echo IP2
echo Player2.crt
echo IP3
echo Player3.crt
echo IP4
echo Player4.crt
echo IP5
echo Player5.crt
echo IP6
echo Player6.crt
echo IP7
echo Player7.crt
echo IP8
echo Player8.crt
echo IP9
echo Player9.crt`

For each node $i, change IP$i to 127.0.0.1

Run:
`cp Auto-Test-Data/1/* Data/`

`./cert.sh | ./Setup.x`

`./Setup.x` with inputs: 2 -> 2 -> p -> 4 (p listed below)

p = 3608870760655701536654448303084521404059979435669688520664454167677047564331360806878098945169255539464747077653151390316596266506041127794233364507011499768902844417

Set bash variable i=1 -> 10 for corresponding machines

Running computation:

Copy files input.sh and ec2_benchmark.sh into this folder.

Run keygen first:
`./ec2_benchmark.sh $i Programs/secret_keygen`

Then setup and run decrypt:
`./input.sh >> ~/SCALE-MAMBA/Data/Player${i}_in.txt`

`cp ~/SCALE-MAMBA/Data/Player${i}_shareout.txt ~/SCALE-MAMBA/Data/Player${i}_sharein.txt`

`./ec2_benchmark.sh $i Programs/dec_test `


Timing and communication costs will be output to the command line.


Results we got (note that distributing the costs over multiple nodes make the costs lower than they are in a simulation on one machine):

With t2.xlarge (16GB RAM)

5 parties:
computation:  84 seconds
bandwidth:  950848352bytes

10 parties:
computation: 180.49 seconds
bandwidth:  4487875435 bytes

15 parties:
computation:  382 seconds
bandwidth:   12427673470bytes

