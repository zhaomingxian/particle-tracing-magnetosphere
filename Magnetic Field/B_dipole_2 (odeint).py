#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 12:06:40 2017

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
m = np.array([0.0, 0.0, 10000]) 
r0 = np.array([0.0, 0.0, 0.0])

def b_field(m, r, r0):
    r_diff = r - r0
    r_mag = np.linalg.norm(r_diff)
    term1 = 3.*r_diff*(np.dot(m, r_diff))/r_mag**5
    term2 = m/r_mag**3
    B = mu*(term1 - term2)/(4*np.pi)
    uniform = [0,0,5e-9]    # option for constant B field
    return B

def deriv(x,t):
    xx, xy, xz = x[0], x[1], x[2]
    vx, vy, vz = x[3], x[4], x[5]
    x=np.array([xx, xy, xz])
    v=np.array([vx, vy, vz])
    B = b_field(m, x, r0)
    a = (q * np.cross(v,B) / mp)
    return (vx, vy, vz, a[0], a[1], a[2])

#def b_field_values():
#    pos = np.linspace(-60, 60, 120)
#    b = b_field(m,[pos,pos,pos],r0)
#    return b
#
#pos = np.linspace(-60, 60, 120)
#x = b_field(m,[pos,pos,pos],r0)
#print x
    
xinit = [-10, 0.0, 0.0, 100, 0.0, 0.0]
binit = np.linalg.norm(b_field(m,[xinit[0],xinit[1],xinit[2]],r0))
r = mp*xinit[3]/(q*binit)   # Larmar radius
T = 2*np.pi*r/xinit[3]      # Gyroperiod particle drift
print r
print T

t = np.linspace(0,10,1000)*10*T

soln = spi.odeint(deriv,xinit,t)
print np.shape(soln)

x = soln[:,0]  
y = soln[:,1]   
z = soln[:,2]
vx = soln[:,3]  
vy = soln[:,4] 
vz = soln[:,5]

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

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x,y,z)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.show()