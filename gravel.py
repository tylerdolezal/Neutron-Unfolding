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
    chi2n0 = 0 ; dx0 = 1 ; ddx = 1
    error = []
    stepcount = 1
    while ddx > tolerance:
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

        chi2n = sum((rdot-data)**2) / sum(rdot)
        dx = chi2n0-chi2n
        ddx = abs(dx-dx0)
        chi2n0 = chi2n
        error.append(ddx)
        print("Iteration {}, dx = {}".format(stepcount,ddx))
        stepcount += 1

        dx0 = dx

    return(x,np.array(error))
