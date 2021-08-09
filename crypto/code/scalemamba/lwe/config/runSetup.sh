# This script assumes that the conversion circuit in ~/config
#   was generated using the prime used in genSecretSharingOptions.sh

N_PLAYERS=$1
THRESHOLD=$2  # Require 2*THRESHOLD < N_PLAYERS

bash ./genCertOptions.sh ${N_PLAYERS} ${THRESHOLD} | ./Setup.x

bash ./genSecretSharingOptions.sh ${N_PLAYERS} ${THRESHOLD} | ./Setup.x

cp ~/config/ConversionCircuit-LSSS_to_GC.txt ./Data/
