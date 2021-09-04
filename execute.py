import numpy as np
import pandas as pd
import seaborn as sns
from mlem import mlem
from gravel import gravel
import matplotlib.pyplot as plt
from response_matrix import response_matrix
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

sns.set_theme()
sns.set_style('ticks')
plt.rc('font', family='serif')

def execute(initial_guess):
    """
    initial_guess --> 0 for constant and 1 for ToF initial guess
    """
    #----------------------------------------
    # Response matrix import
    #----------------------------------------
    R = response_matrix()
    n,m = R.shape[0],R.shape[1]
    #----------------------------------------
    # Pulse height import
    #----------------------------------------
    dir = "unfolding_inputs/"
    neutrons = pd.read_csv(dir+"reduced_data.csv")
    N1 = neutrons["NEUTRON 1"]
    N2 = neutrons["NEUTRON 2"]
    #----------------------------------------
    # Initial guess
    #----------------------------------------
    true_data = np.loadtxt(dir+"energy-spectrum.txt")
    xtrue,xbins = true_data[0],true_data[1]
    x = np.ones((m,))
    #----------------------------------------
    # Execute the two algorithms
    #----------------------------------------
    if initial_guess == 0:
        tol = 0.2
        xg,errorg = gravel(R,N1,x,tol)
        xm,errorm = mlem(R,N1,x,tol)
        suffix = "constant"
    else:
        tol = 0.8
        xg,errorg = gravel(R,N1,xtrue,tol)
        xm,errorm = mlem(R,N1,xtrue,tol)
        suffix = "true"

    fig,ax = plt.subplots()
    #-----------------------------------------
    # Normalize the vectors
    #-----------------------------------------
    Lt = np.linalg.norm(xtrue) ; xtrue = xtrue/Lt
    Lg = np.linalg.norm(xg); xg = xg/Lg
    Lm = np.linalg.norm(xm); xm = xm/Lm
    #-----------------------------------------
    # plot GRAVEL results against ToF
    #-----------------------------------------
    ax.plot(xbins,(xtrue),color="k",label = "ToF Spectrum",alpha = 0.3)
    ax.plot(xbins,(xg),label="GRAVEL")
    ax.grid(which="major",alpha=0.6)
    ax.grid(which="minor",alpha=0.3)
    ax.set_xlabel("Neutron Energy (MeV)")
    ax.set_ylabel("Normalized Counts")
    ax.set_ylim(0,0.175)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.legend(frameon=False)
    plt.savefig("final-results/real-data-gravel-{}.png".format(suffix),dpi=300,bbox_inches="tight")

    plt.close()
    #-----------------------------------------
    # plot MLEM results against ToF
    #-----------------------------------------
    fig,ax = plt.subplots()
    ax.plot(xbins,(xtrue),color="k",label = "ToF Spectrum",alpha=0.3)
    ax.plot(xbins,(xm),label="MLEM")
    ax.grid(which="major",alpha=0.6)
    ax.grid(which="minor",alpha=0.3)
    ax.set_xlabel("Neutron Energy (MeV)")
    ax.set_ylabel("Normalized Counts")
    ax.set_ylim(0,0.175)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.legend(frameon=False)
    plt.savefig("final-results/real-data-mlem-{}.png".format(suffix),dpi=300,bbox_inches="tight")

    plt.close()
    #--------------------------------------------------
    # Plot GRAVEL and MLEM overtop one another
    #--------------------------------------------------
    fig,ax = plt.subplots()
    ax.plot(xbins,(xtrue),color="k",label = "ToF Spectrum",alpha = 0.3)
    ax.plot(xbins,(xg),label="GRAVEL")
    ax.plot(xbins,(xm),label="MLEM")
    ax.grid(which="major",alpha=0.6)
    ax.grid(which="minor",alpha=0.3)
    ax.set_xlabel("Neutron Energy (MeV)")
    ax.set_ylabel("Normalized Counts")
    ax.set_ylim(0,0.175)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.legend(frameon=False)
    plt.savefig("final-results/both-{}.png".format(suffix),dpi=300,bbox_inches="tight")
    plt.close()
    #--------------------------------------------------
    # relative error between ToF, GRAVEL and MLEM
    #--------------------------------------------------
    fig,ax = plt.subplots()
    #--------------------------------------------------
    # remove all instances of 0 before calculating relative error
    #--------------------------------------------------
    xbins = np.array([xbins[i] for i in range(m) if xtrue[i] != 0])
    xg = np.array([xg[i] for i in range(m) if xtrue[i] != 0])
    xm = np.array([xm[i] for i in range(m) if xtrue[i] != 0])
    xtrue = np.array([x for x in xtrue if x != 0])
    diff_g = abs(xtrue-xg) / xtrue; diff_m = abs(xtrue-xm) / xtrue
    np.savetxt("final-results/relative-norm-{}.txt".format(suffix), [np.linalg.norm(diff_g),np.linalg.norm(diff_m)])
    #-----------------------------------------
    # plot error versus iteration
    #-----------------------------------------
    fig,ax = plt.subplots()
    ax.plot(np.arange(len(errorg)),errorg,color ="k",label="GRAVEL")
    ax.plot(np.arange(len(errorm)),errorm,label="MLEM")
    ax.set_ylim(-5,15)
    ax.axhline(tol,color="r",linewidth=0.75)
    ax.grid(which="major",alpha=0.6)
    ax.grid(which="minor",alpha=0.3)
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.set_ylabel("$\Delta$J")
    ax.set_xlabel("Iteration")
    text = "$\Delta$J$_{stop}$"
    fig.text(0.70,0.15,text+" = {}".format(tol))
    ax.legend(frameon=False)

    plt.savefig("final-results/error-{}.png".format(suffix),dpi=300,bbox_inches="tight")
    plt.close()

    #-----------------------------------------
    # plot a bar chart showing the norms of
    # the relative error vectors
    #-----------------------------------------
    truenorm = np.loadtxt("final-results/relative-norm-true.txt")
    xgtrue,xmtrue = truenorm[0],truenorm[1]

    constnorm = np.loadtxt("final-results/relative-norm-constant.txt")
    xgconst,xmconst = constnorm[0],constnorm[1]

    fig,ax = plt.subplots(figsize=(6,4))

    ax.bar([1,2],[xgtrue,xmtrue],width = 0.35, label="a priori",edgecolor="black")
    ax.bar([3,4],[xgconst,xmconst],width = 0.35,label = "constant",edgecolor="black")

    for bar in ax.patches:
        bar_value = bar.get_height()
        text = '{:.2f}'.format(bar_value)
        text_x = bar.get_x() + bar.get_width() / 2
        text_y = (bar.get_y() + bar_value)
        ax.text(text_x, text_y, text, ha='center', va='bottom')

    plt.xticks([1,2,3,4],["GRAVEL", "MLEM", "GRAVEL", "MLEM"])
    plt.ylabel("Relative Error")
    plt.ylim(0,12)
    plt.legend(frameon=False,loc="upper left")
    plt.savefig("final-results/relative-error.png",dpi=300,bbox_inches="tight")
    plt.close()

#-----------------------------------------
# execute takes one input which tells it
# which initial guess to use
#-----------------------------------------
constant = 0 ; tof = 1
execute(tof)
