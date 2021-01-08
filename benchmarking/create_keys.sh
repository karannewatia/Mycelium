# I have never actually run this. 
# This is just a (hopefully accurate) record of what I did in terminal
key_name=$1

aws ec2 create-key-pair --keyname ${key_name} > ~/Downloads/${key_name}.info

cat ~/Downloads/${key_name}.info | tail -n +2 | head -n -3 | sed 's/.*BEGIN/-----BEGIN/' | sed 's/",//' | sed  's/\\n/\n/g' > ~/Downloads/${key_name}.pem

chmod 400 ~/Downloads/${key_name}.info
chmod 400 ~/Downloads/${key_name}.pem
