import math
import random

def mpc_dec_input():
    print(5)
    print(10)
    for i in range(2*32768):
        print(1)

def decompose_gadget():
    for i in range(63, -1, -1):
        if (i>=64):
            print(2**63)
        else:
            print(2**i)

#q -> ciphertext modulus
#t -> plaintext modulus
#n -> degree of polynomial
#D-> number of multiplications
#A -> number of addtions after D multiplications
def mult_noise(q,t,n,D, A=1000000000):
    noise = 4*((2*t*math.sqrt(n))**(D+1))*((2*n)**(D/2)) * math.sqrt(A)
    return q >= noise

def main():
    #decompose_gadget()
    #mpc_dec_input()
    print(mult_noise((1<<550)+1, 2**30, 2**15, 10))


if __name__ == '__main__':
    main()
