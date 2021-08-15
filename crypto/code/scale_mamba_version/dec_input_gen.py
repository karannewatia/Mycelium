import math

#Generate the input used for decryption in the MPC
#n is the polynomial degree
def mpc_dec_input(n):
    #assumes that the plaintext length is 12
    print(5) #bin 1 is in the range of 0 to 5 (both inclusive)
    print(11) #bin 2 is in the range of 6 to 11 (both inclusive)
    #can change the plaintext length/bin ranges/add more bins as needed (though this requires changing the binning logic in source/fhe_test.mpc)

    for i in range(2*n):
        #dummy ciphertext used for benchmark the costs since the costs are input-oblivious
        print(1)


def main():
    mpc_dec_input(32768)


if __name__ == '__main__':
    main()
