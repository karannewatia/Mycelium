import sys

def gen_input(N):

    # Can set inputs to other things! These are arbitrary vectors
    u = [1]*(10*N)
    v = [1]*(10*N)
    res_u = [1]*N
    res_v = [1]*N

    print(*u, *v, *res_u, *res_v)

gen_input(int(sys.argv[1]))


