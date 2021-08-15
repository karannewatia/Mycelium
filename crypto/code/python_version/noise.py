import math

#This function is used to check whether, for a given set of parameters (q,t,n),
#it is possible to perform D multiplications followed by A additions.
#Returns True if it's possible, and False if not.
#q -> ciphertext modulus
#t -> plaintext modulus
#n -> degree of polynomial
#D-> number of multiplications
#A -> number of addtions after D multiplications
def mult_noise(q,t,n,D,A=1000000000):
    noise = 4*((2*t*math.sqrt(n))**(D+1))*((2*n)**(D/2)) * math.sqrt(A)
    return q >= noise

def main():
    t = 2**30
    n = 2**15
    q = 3608870760655701536654448303084521404059979435669688520664454167677047564331360806878098945169255539464747077653151390316596266506041127794233364507011499768902844417
    print(mult_noise(q, t, n, 10))

if __name__ == '__main__':
    main()
