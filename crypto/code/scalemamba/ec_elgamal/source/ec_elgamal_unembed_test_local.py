import sys
import os
sys.path.append(os.path.abspath("/root/SCALE-MAMBA/Programs/ec_elgamal/"))

from ec_elgamal_lib import discrete_log_id
from ec_elgamal_lib import discrete_log_io

from sys import argv

playerId = int(argv[1])
fout = open('Data/Player' + str(playerId) + '_in.txt', 'w')
fin = open('Data/Player' + str(playerId) + '_out.txt', 'r')

nPlayers = int(argv[2])

while True:

  command = int(fin.readline())

  if command == discrete_log_id():
    discrete_log_io(fin, fout, playerId, nPlayers)



  
