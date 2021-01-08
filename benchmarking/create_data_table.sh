
test_name=$1   # e.g. ec_elgamal_dec
lgm=$2         # e.g. 20
l=$3

echo "n_parties, communication (MB), run_time (s)" > ../data/${test_name}_lgm=${lgm}.csv; 
for i in $( find . -regex "./results/"${test_name}"_test_[0-9]*_.*l=.*" | grep -o test_[0-9]* | grep -o [0-9]* | sort -g | uniq ); do
  comm=$( cat results/${test_name}_test_${i}_lgm=${lgm}_l=${l}.comm | grep -o [0-9]* ); 
  comm=$( echo "print(${comm}/(1024*1024))" | python3 )
  runtime=$( cat results/${test_name}_test_${i}_lgm=${lgm}_l=${l}.run_time | grep -o [0-9]* ); 
  runtime=$( echo "print(${runtime}/1000)" | python3 )
  echo ${i}, ${comm}, ${runtime} >> ../data/${test_name}_lgm=${lgm}.csv; 
done
