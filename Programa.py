# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 21:28:10 2021

@author: Jordi
"""

# SIMULACIÓ D'UNA DIMENSIÓ

# Importing necessary packages (s'explicarà què fa cada un a la classe)
from os import kill
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
#%matplotlib inline # If using Jupyter, uncomment this line!

# Constants
g = 9.81           # acceleració de la gravetat [m/s^2]
rho_0 = 1.225      # Densitat al nivell del mar [kg/m^3]
H = 8800           # Escala de l'alçada [m]
c_D = 0.54         # Coeficient del drag del coet [-]
A = 0.0103         # Àrea frontal del coet [m^2]
m_i = 19.1         # Massa "molla" del coet (inclou propel·lent) [kg]
m_f = 10.604       # Massa "seca" del coet (no inclou propel·lent) [kg]
T_avg = 2601.8     # Thrust mitjà del coet [N]
t_burn = 6.09      # Temps de cremat [s]

# Si guardem alguns paràmetres ens estalviarem temps:
m = (m_i + m_f)/2 # Massa mitjana del coet
k = 0.5*c_D*A*rho_0 # Factor constant en l'equació del Drag

def Thrust(t): #Revisa si el temps de cremat es superior o igual al temps acutal
    """ La curva del Thrust del motor.
    Paràmetre:
        t temps [s]
    """
    if t < t_burn:
        return T_avg
    return 0

def Drag(h, v): #Drag Actual del coet
    """ Drag de l'aire
    Paràmetres:
    h altitud [m]
    v velocitat [m/s]
    """
    if v == 0: # Amb això ens estalviem dividir per 0.
        return 0
    return -k*np.exp(-h/H)*v*abs(v)

def f(t, w):
    """ Part dreta de les equacions diferencials, també en parlarem a classe.
    Paràmetres:
    t temps [s]
    w vector amb les coordenades necessàries i velocitats.
    En el cas d'una dimensió, w = (r, v)
    """
    temp_vector = np.zeros(2)
    # Eq. (3) (1D)
    temp_vector[0] = w[1]
    # Eq. (4). In the 1D-case, r_y = r = h
    temp_vector[1] = (Thrust(t) + Drag(w[0],w[1]))/m - g
    return temp_vector

def trajectory(dt, t_f):
    """ Calcula la trajectòria del coet  a partir d'equacions diferencials
    utilitzant el package scipy que hem introduit a l'inici.
   
    Paràmetres:
    dt temps step [s]
    t_f temps final [s]
    Torna:
    solution.t Valors de temps calculats
    solution.y[0] valors de la posició-y del coet (altitud)
    solution.y[1] valors de la velocitat-y del coet
    """
    t_span = [0, t_f] # interval d'integració
    w_0 = [0, 0] # valors inicials
    t_val = np.arange(0, t_f, dt) # valors de temps
    
    solution = solve_ivp(f, t_span, w_0, t_eval=t_val)
    
    return solution.t, solution.y[0], solution.y[1]

#Aquests valors fan referència al que ultilitzarà el programa per integrar:
dt=0.02
t_f=120
s = 0
# Gràfic de la trajectòria
t, y, v_y = trajectory(dt,t_f)

plt.plot(t,y,'r')
plt.title("Trajectory")
plt.xlabel("$t$ [s]")
plt.ylabel("altitude [m]")
plt.axis([0, 100, 0, 11000])
plt.grid(True)
plt.show()

#Gràfic de la velocitat
plt.plot(t,v_y,'r')
plt.title("Velocity")
plt.xlabel("$t$ [s]")
plt.ylabel("velocity [m/s]")
plt.axis([0, 100, -300, 750])
plt.grid(True)
plt.show()
