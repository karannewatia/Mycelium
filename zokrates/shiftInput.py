import sys

# Can set inputs to other things
def gen_input(N):
    u = [1]*N
    res_u = [1]*N
    v = [2]*N
    res_v = [2]*N
    for i in range(N):
        res_u[i] = u[i]*x[i]
        res_v[i] = v[i]*x[i]

    print(*u, *v, *res_u, *res_v, *x)

gen_input(int(sys.argv[1]))


