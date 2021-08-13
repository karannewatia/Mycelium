**************************************************************************
Benchmarking Suite for testing MPC Key Generation and Decryption protocols
**************************************************************************

These scripts allow for AWS instances to easily be created and for
programs testing key generation and decryption.

# Create AWS CLI ACCOUNT
First set up an AWS account with ssh access.
Store the ssh key in ~/Downloads/AWScis.pem
See AWS_CLI_INSTRUCTIONS.txt for details on this process.

# CREATE AN IMAGE
To create an image for the protocol you want to test.
$ ./create_ami.sh src_local image_name
> Here src_local is the local path to the relevant source repo.

This will create a new AWS image which contains
a docker of all the keygen/dec implementation stored at src_local.
The image id will be stored in image_name.ami_id

# CREATE INSTANCES
Next, create several instances of the image you want to run.

Decide on the number of players, n_players, and the maximum number of malicious
players, threshold, that the system should support. Then execute:
$ ./create_players.sh n_players threshold image_name

This will create n_players instances. 
The IP addresses will be stored in ip_addresses.txt
It will configure the system to handle threshold malicious parties.

# RUN TESTS
To run a particular program, execute the following:
$ ./run_test.sh n_players threshold program n_io local_in local_out

n_players, threshold: the same as for ./create_players.sh.
program: the name of the particular test being run 
  (e.g. key generation and decryption should be different tests).
n_io: the amount of input_ouput needed by each player.
  If you don't know, put 0 (corresponds to infinity)
  If there is no IO, put 1 (smallest value)
local_in: true or false. Do players supply dynamic input to the protocol?
local_out: true or false. Do players dynamically process output from protocol?

The benchmarking metrics will be saved to the results dir.

# CLEAN UP
To avoid being charged unnecessarily, run the terminate script when you are done.
$ ./terminate_all.sh
