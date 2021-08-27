import numpy as np
import pandas as pd
import myfuncs as fun
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

sns.set_theme()
sns.set_style('ticks')
plt.rc('font', family='serif')

#----------------------------------------
# Response matrix import
#----------------------------------------
R = fun.response_matrix()
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
# use xtrue for ToF initial guess and
# x = np.ones((m,)) for constant initial guess
#----------------------------------------
# Execute the two algorithms
#----------------------------------------
tol = 1e-2
xg,errorg = fun.gravel(R,N1,xtrue,tol)
xm,errorm = fun.mlem(R,N1,xtrue,tol)

fig,ax = plt.subplots()
Lt = np.linalg.norm(xtrue)
Lg = np.linalg.norm(xg)
Lm = np.linalg.norm(xm)
#-----------------------------------------
# plot GRAVEL results against ToF
#-----------------------------------------
ax.plot(xbins,(xtrue/Lt),color="k",label = "ToF Spectrum",alpha = 0.3)
ax.plot(xbins,(xg/Lg),label="GRAVEL")
ax.grid(which="major",alpha=0.6)
ax.grid(which="minor",alpha=0.3)
ax.set_xlabel("Neutron Energy (MeV)")
ax.set_ylabel("Normalized Counts")
ax.xaxis.set_minor_locator(MultipleLocator(1))
plt.legend(frameon=False)
plt.savefig("final-results/real-data-gravel-true.png",dpi=300,bbox_inches="tight")

plt.close()
#-----------------------------------------
# plot MLEM results against ToF
#-----------------------------------------
fig,ax = plt.subplots()
ax.plot(xbins,(xtrue/Lt),color="k",label = "ToF Spectrum",alpha=0.3)
ax.plot(xbins,(xm/Lm),label="MLEM")
ax.grid(which="major",alpha=0.6)
ax.grid(which="minor",alpha=0.3)
ax.set_xlabel("Neutron Energy (MeV)")
ax.set_ylabel("Normalized Counts")
ax.xaxis.set_minor_locator(MultipleLocator(1))
plt.legend(frameon=False)
plt.savefig("final-results/real-data-mlem-true.png",dpi=300,bbox_inches="tight")

plt.close()
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
fig.text(0.55,0.15,"Stop Condition = {}".format(tol))
ax.legend(frameon=False)

plt.savefig("final-results/error-true.png",dpi=300,bbox_inches="tight")
plt.close()
