

import sys
import numpy as np
print("\nInput: inlet velocity, reference length scale\n")


U = float(sys.argv[1]); # inlet velocity
print("Incoming velocity is "+str(U)+" m/s")

L0=float(sys.argv[2])  #mm  twine diameter
print("Reference length scale is "+str(L0)+" m")

# Constant in the model
C_u = 0.09
# Calculation
mu=1.307e-6   # kinematic viscosity at 10 degree

Re = U*L0/mu
print("Reynold number is  "+ str(round(Re,2)))

I = 0.16*Re**(-0.125); # turbulence intensity. for fully developed pipe flow

k = 1.5*pow(U*I,2)  #  the turbulent kinetic energy for isotropic turbulence

epsilon = pow(C_u,0.75)*pow(k,1.5)/L0

omega = pow(C_u,-0.25)*pow(k,0.5)/L0

print("Turbulence intensity is "+str(round(I,4)))
print("k is "+str(round(k,8)));
print("epsilon is "+str(round(epsilon,8)))
print("omega is "+str(round(omega,8)))
