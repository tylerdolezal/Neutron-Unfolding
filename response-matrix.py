import numpy as np


def response_matrix():
    with open("unfolding_inputs/response-matrix.txt") as f:
        R = f.readlines()

    for i in range(len(R)):
        R[i] = np.asarray(R[i].split(','),dtype=float)
    R = np.array(R) ; R = R.T
    ## R.shape = (1024,201) which is between [0.1,10.1] MeV
    return(R)
