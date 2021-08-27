import numpy as np


def mlem(R,data,x,tolerance):
    """
    R --> Response matrix, shape is (n,m)
    N --> pulse height spectrum, shape is (n,)
    x --> initial guess at neutron spectrum, shape is (m,)
    tolerance --> user-defined stopping condition
    """
    x = x.copy()
    n = len(data) # true is the recorded specturm
    m = len(x)
    J0 = 0 ; dJ0 = 1 ; ddJ = 1
    error = []
    stepcount = 1
    while ddJ > tolerance:
        vector = np.zeros((n,))
        q = np.zeros((n,))
        for i in range(n):
            factor = (R[i,:]@x)
            vector[i] = data[i]/factor
            q[i] = factor

        for j in range(m):
            term = np.dot(R[:,j],vector)
            x[j] *= (1 / sum(R[:,j]))*term


        J = sum((q-data)**2) / sum(q)
        dJ = J0 - J
        ddJ = abs(dJ-dJ0)
        error.append(ddJ)
        J0 = J
        dJ0 = dJ
        print("Iteration {}, dJ = {}".format(stepcount,ddJ))
        stepcount += 1


    return(x,np.array(error))
