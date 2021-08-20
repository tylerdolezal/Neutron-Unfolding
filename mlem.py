import numpy as np


def mlem(R,N,x,steps):
    n = len(N) # true is the recorded specturm
    m = len(x)

    error = np.ones((steps+1,))
    for astep in range(steps+1):
        vector = np.zeros((n,))
        q = np.zeros((n,))
        for i in range(n):
            factor = (R[i,:]@x)
            vector[i] = N[i]/factor
            q[i] = factor

        for j in range(m):
            term = np.dot(R[:,j],vector)
            x[j] *= (1 / sum(R[:,j]))*term


        J = sum((q-N)**2) / sum(q)
        error[astep] = J
        print("Iteration {}, J = {}".format(astep,J))

    return(x,error)
