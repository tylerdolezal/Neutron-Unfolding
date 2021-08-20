import numpy as np

def gravel(R,data,x,steps):
    m = R.shape[1]
    n = R.shape[0]
    R = np.array([R[i] for i in range(n) if data[i] != 0])
    data = np.array([x for x in data if x > 0])
    n = R.shape[0]

    error = np.ones((steps+1,))
    for astep in range(steps+1):
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

        chi2n = sum((rdot-data)**2 / data) / n
        error[astep] = chi2n
        print("Iteration {}, tolerance = {}".format(astep,chi2n))
