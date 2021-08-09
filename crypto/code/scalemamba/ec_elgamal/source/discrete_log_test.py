from ec_elgamal_lib import discrete_log_kangaroo

from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

g = Point(76049884773772239630286819839663813044215220798366048289168112050194373987235, 111998029357810440620223172064231485820163014246983600027697176972731586228871, secp256k1)

x = 140001

y = g*x

print("x = " + str(x))
print("y = " + str(y))

xPrime = discrete_log_kangaroo(g, 0, 16000000, y)

print("Expect: " + str(x))
print("Actual: " + str(xPrime))
