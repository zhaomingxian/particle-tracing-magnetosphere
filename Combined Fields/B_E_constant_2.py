#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 22:10:40 2017

@author: ricktjwong
"""

import numpy as np
from matplotlib import pyplot as plt
import scipy.integrate as spi
from mpl_toolkits.mplot3d import Axes3D

#plt.rcParams["figure.figsize"] = (4,3)
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['lines.linewidth'] = 0.8

""" Global quantities """

mu = 4*np.pi*1e-7
q = 1.6 * 1e-19
mp = 1.67 * 1e-27
r0 = np.array([0.0, 0.0, 0.0])

""" Initial conditions"""
B = [0, 0, 1e-5]
E = np.array([1e-4, 0, 0])
xinit = [-10, 0.0, 0.0, 0.0, 0.0, 0.0]
x0 = np.array([xinit[0], xinit[1], xinit[2]])
v0 = np.array([xinit[3], xinit[4], xinit[5]])

def deriv(x,t):
    xx, xy, xz = x[0], x[1], x[2]   # Initial conditions position
    vx, vy, vz = x[3], x[4], x[5]   # Initial conditions velocity
    x=np.array([xx, xy, xz])
    v=np.array([vx, vy, vz])
    a = q * (np.cross(v,B) + E) / mp
    return (vx, vy, vz, a[0], a[1], a[2])

binit = np.linalg.norm(B)
r = mp*xinit[3]/(q*binit)   # Larmar radius
T = 2*np.pi*r/xinit[3]      # Gyroperiod particle drift
print r
print T

t = np.linspace(0,0.1,1000)

soln = spi.odeint(deriv,xinit,t)    # Solve ODE

x, y, z = soln[:,0], soln[:,1], soln[:,2]
vx, vy, vz = soln[:,3], soln[:,4], soln[:,5]

plt.figure(1)
plt.plot(x,y)
#plt.xlim([-600-3.04e7,-3.04e7])
#plt.ylim([0,600])
plt.xlabel("position, x")
plt.ylabel("position, y")

plt.figure(2)
plt.plot(x,z)
plt.xlabel("position, x")
plt.ylabel("position, z")

fig = plt.figure(3)
ax = fig.add_subplot(111, projection='3d')
ax.plot(x,y,z)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.show()

"""Energy Calculations"""

v_xyz = np.vstack((vx,vy,vz)).T
v_ = []
for i in v_xyz:
    v_.append(np.linalg.norm(i))
v_ = np.array(v_)
KE = 0.5*mp*v_**2
KE_ave = np.average(KE)
KE_var = np.var(KE)
print KE_ave

posr = np.vstack((x,y,z)).T
PE = []
for i in posr:
    PE.append(q*np.dot(i-x0, E))
#print PE

plt.figure(4)
plt.plot(t, PE)
plt.xlabel("Time (s)")
plt.ylabel("PE")

TE = []
for i,j in zip(KE, PE):
    TE.append(i+j)

plt.figure(5)
plt.plot(t, TE)
plt.xlabel("Time (s)")
plt.ylabel("TE")
    
plt.figure(6)
fig2, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax3 = ax1.twinx()
#ax1.plot(t,v_,'b')
ax2.plot(t,KE,'r')
#ax3.plot(t,PE,'g')
ax1.set_xlabel('time/s')
ax1.set_ylabel('|v|', color='blue')
ax1.tick_params('b', colors='blue')

ax2.set_ylabel('KE', color='r')
ax2.tick_params('r', colors='r')

#ax1.set_xlim(left=0, right=0.02)
#ax2.set_xlim(left=0, right=0.02)


