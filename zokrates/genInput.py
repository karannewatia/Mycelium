import sys

def gen_input(N):
    z = [1]*N
    a = [1]*N
    b = [2]*N

 
    e0 = [1]*N
    e1 = [2]*N
    e2 = [2]*N

    u = [0]*N
    v = [0]*N
    for i in range(N):
        u[i] = a[i]*e0[i] + 2*e1[i]
        v[i] = b[i]*e0[i] + 2*e2[i] + z[i]
    

    print(*z, *a, *b, *u, *v)

gen_input(int(sys.argv[1]))


