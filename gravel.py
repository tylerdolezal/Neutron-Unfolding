import numpy as np
from numpy import log,exp

def gravel(R,data,x,tolerance):
    """
    R --> Response matrix, shape is (n,m)
    N --> pulse height spectrum, shape is (n,)
    x --> initial guess at neutron spectrum, shape is (m,)
    tolerance --> user-defined stopping condition
    """
    x = x.copy()
    n = R.shape[0]
    m = R.shape[1]
    # eliminate any channel with 0 count
    R = np.array([R[i] for i in range(n) if data[i] != 0])
    data = np.array([x for x in data if x > 0])
    # redefine number of rows after the reduction
    n = R.shape[0]
    J0 = 0 ; dJ0 = 1 ; ddJ = 1
    error = []
    stepcount = 1
    while ddJ > tolerance:
        W = np.zeros((n,m))
        rdot = np.zeros((n,))
        for i in range(n):
            rdot[i] = (R[i,:]@x)

        for j in range(m):

            W[:,j] = data*R[:,j]*x[j] / rdot
            num = np.dot(W[:,j],log(data/rdot))

            num = np.nan_to_num(num)
            den = sum(W[:,j])

            if den == 0:
                x[j] *= 1
            else:
                x[j] *= exp(num/den)

        J = sum((rdot-data)**2) / sum(rdot)
        dJ = J0-J
        ddJ = abs(dJ-dJ0)
        J0 = J
        error.append(ddJ)
        print("Iteration {}, ddJ = {}".format(stepcount,ddJ))
        stepcount += 1
        dJ0 = dJ

    return(x,np.array(error))
