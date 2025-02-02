#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 14:35:03 2017

@author: ricktjwong
"""

import numpy as np
from matplotlib import pyplot as plt
import scipy.integrate as spi
from mpl_toolkits.mplot3d import Axes3D

""" Global quantities """

mu = 4*np.pi*1e-7
q = 1.6 * 1e-19
mp = 1.67 * 1e-27
m = np.array([0.0, 0.0, 1e5]) 
r0 = np.array([0.0, 0.0, 0.0])
RE = 6.4e6

def b_field(m, r, r0):
    r_diff = r - r0
    r_mag = np.linalg.norm(r_diff)
    term1 = 3.*r_diff*(np.dot(m, r_diff))/r_mag**5
    term2 = m/r_mag**3
    B = mu*(term1 - term2)/(4*np.pi)
    uniform = [0,0,5e-9]    # option for constant B field
    return B

def deriv(x,t):
    xx, xy, xz = x[0], x[1], x[2]   # Initial conditions position
    vx, vy, vz = x[3], x[4], x[5]   # Initial conditions velocity
    x=np.array([xx, xy, xz])
    v=np.array([vx, vy, vz])
    B = b_field(m, x, r0)
    a = q * (np.cross(v,B) + E) / mp
    return (vx, vy, vz, a[0], a[1], a[2])
    

xinit = [-10, 0.0, 0.0, 1000, 0.0, 0.0]
#xinit = [-5*RE, 0.0, 0.5*RE, 1e8, 0.0, 0.0]
E = np.array([0, 0, 0])
binit = np.linalg.norm(b_field(m,[xinit[0],xinit[1],xinit[2]],r0))
r = mp*xinit[3]/(q*binit)   # Larmar radius
T = 2*np.pi*r/xinit[3]      # Gyroperiod particle drift
print r
print T

t = np.linspace(0,10,1000)

soln = spi.odeint(deriv,xinit,t)    # Solve ODE

x, y, z = soln[:,0], soln[:,1], soln[:,2]
vx, vy, vz = soln[:,3], soln[:,4], soln[:,5]


fig = plt.figure(1)
ax = fig.add_subplot(1, 1,1)
ax.set_aspect(1)
ax.plot(x,y)
ax.set_title('X against Y')
#plt.xlim([-600-3.04e7,-3.04e7])
#plt.ylim([0,600])
ax.set_aspect('equal')
plt.xlabel("X axis")
plt.ylabel("Y-axis")

plt.figure(2)
plt.plot(x,z)
plt.title('X against Z')
plt.xlabel("X axis")
plt.ylabel("Z-axis")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x,y,z)

ax.set(xlim=[-12,12],ylim=[-12,12],zlim=[-12,12])
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.show()

posr = np.vstack((x,y,z)).T

def CheckEnter(r):
     for i in r:
        dist = np.linalg.norm(i)
        if dist < RE :
            print "Enter"
        elif dist > RE :
            print "did not enter"
            print dist
#Track = CheckEnter(posr)
            