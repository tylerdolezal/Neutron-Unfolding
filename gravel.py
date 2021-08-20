import numpy as np

def gravel(R,N,x,steps):
    """
    R --> Response matrix, shape is (n,m)
    N --> pulse height spectrum, shape is (n,)
    x --> initial guess at neutron spectrum, shape is (m,)
    steps --> max number of iterations to perform
    """
    m = R.shape[1]
    n = R.shape[0]
    R = np.array([R[i] for i in range(n) if N[i] != 0])
    N = np.array([x for x in N if x > 0])
    n = R.shape[0]

    error = np.ones((steps+1,))
    for astep in range(steps+1):
        W = np.zeros((n,m))
        rdot = np.zeros((n,))
        for i in range(n):
            rdot[i] = (R[i,:]@x)

        for j in range(m):

            W[:,j] = N*R[:,j]*x[j] / rdot
            num = np.dot(W[:,j],log(N/rdot))

            num = np.nan_to_num(num)
            den = sum(W[:,j])

            if den == 0:
                x[j] *= 1
            else:
                x[j] *= exp(num/den)

        chi2n = sum((rdot-N)**2 / N) / n
        error[astep] = chi2n
        print("Iteration {}, tolerance = {}".format(astep,chi2n))
