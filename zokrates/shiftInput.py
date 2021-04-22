import sys

def gen_input(N):
    u = [1]*N
    res_u = [1]*N
    v = [2]*N
    res_v = [2]*N
    for i in range(N):
        if (i+5<N):
            res_u[i] = u[i]
            res_v[i] = v[i]
        else:
            res_u[i] = 0    
            res_v[i] = 0    
    

    print(*u, *v, *res_u, *res_v)
    #print(*u, *v)

gen_input(int(sys.argv[1]))


