import math

def mpc_dec_input(n):
    print(5)
    print(10)
    for i in range(2*n):
        print(1)

#q -> ciphertext modulus
#t -> plaintext modulus
#n -> degree of polynomial
#D-> number of multiplications
#A -> number of addtions after D multiplications
def mult_noise(q,t,n,D,A=1000000000):
    noise = 4*((2*t*math.sqrt(n))**(D+1))*((2*n)**(D/2)) * math.sqrt(A)
    return q >= noise

def main():
    #mpc_dec_input(3)
    print(mult_noise((1<<550)+1, 2**30, 2**15, 10))


if __name__ == '__main__':
    main()
