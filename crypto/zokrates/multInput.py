import sys

def gen_input(N):

    # Can set inputs to other things! These are arbitrary vectors
    u = [1]*N
    v = [2]*N

    print(*u, *v)

gen_input(int(sys.argv[1]))


