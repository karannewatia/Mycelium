import math
import numpy as np
import random

def exp_sample(mean):
    return -mean*math.log(random.random())

def laplace(scale):
    e1 = exp_sample(scale)
    e2 = exp_sample(scale)
    return e1 - e2

def ones():
    #for i in range(2*2048*64):
    for i in range(2*32768):
        print(1)

def g():
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
    noise = 4*((2*t*math.sqrt(n))**(D+1))*((2*n)**(D/2)) * A
    return q >= noise

def graph_a(f, C):
    p = math.exp(-f*C)
    p *= (5*math.e*f/2)**(2*C/5)
    return 2*p*10

def graph_b(f, g, C):
    size = math.exp(-(f+g)*C)
    size *= (5*math.e*(f+g))**(C/5)
    return size

def main():
    #print(laplace(10))

    #g()
    ones()

    # result = graph_a(0.02, 10)
    # print(result)
    # result = graph_b(0.00, 0.04, 10)
    # print(result)

    # tmp = 5213351276381234054160419996566192858185969047516585959753981767067331398195163076515879100938499184364596466644818565365410708138306357824139022410186753
    # print(mult_noise((1<<437)+1, 2**30, 2**14, 10))


if __name__ == '__main__':
    main()
