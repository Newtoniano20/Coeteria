"""
Forces Class
All Forces that may be applied into rocketry will be defined and merged together
"""
import tkinter

from numpy import zeros, exp, arange
from scipy.integrate import solve_ivp


class Forces:

    def __init__(self, defaults: dict):
        self.H = defaults['H']
        self.t_burn = defaults['t_burn']
        self.T_avg = defaults['T_avg']
        self.g = defaults['g']
        self.m_i = defaults['m_i']
        self.m_f = defaults['m_f']
        self.c_D = defaults['c_D']
        self.A = defaults['A']
        self.rho_0 = defaults['rho_0']
        self.m = (self.m_i + self.m_f) / 2
        self.k = 0.5 * self.c_D * self.A * self.rho_0
        self.dt = defaults['dt']
        self.t_f = defaults['t_f']

    def thrust(self, t: float):
        if t < self.t_burn:
            return self.T_avg
        return 0

    def update_variables(self, var: list):
        """
        Updates all variables following

        :param var: list of entries
        :type var: list
        :return: None
        :rtype:
        """
        self.g = float(var[0].get())  # acceleració de la gravetat [m/s^2]
        self.rho_0 = float(var[1].get())  # Densitat al nivell del mar [kg/m^3]
        self.H = float(var[2].get())  # Escala de l'alçada [m]
        self.c_D = float(var[3].get())  # Coeficient del drag del coet [-]
        self.A = float(var[4].get())  # Àrea frontal del coet [m^2]
        self.m_i = float(var[5].get())  # Massa "molla" del coet (inclou propel·lent) [kg]
        self.m_f = float(var[6].get())  # Massa "seca" del coet (no inclou propel·lent) [kg]
        self.T_avg = float(var[7].get())  # Thrust mitjà del coet [N]
        self.t_burn = float(var[8].get())  # Temps de cremat [s]
        self.m = (self.m_i + self.m_f) / 2
        self.k = 0.5 * self.c_D * self.A * self.rho_0

    def drag(self, h: float, v: float):
        if v == 0:  # Amb això ens estalviem dividir per 0.
            return 0
        return -self.k * exp(-h / self.H) * v * abs(v)

    def paracaigudes(self, v, t):  # todo
        pass

    def f(self, t: float, w: float):
        temp_vector = zeros(2)
        # Eq. (3) (1D)
        temp_vector[0] = w[1]
        # Eq. (4). In the 1D-case, r_y = r = h
        temp_vector[1] = (self.thrust(t) + self.drag(w[0], w[1])) / self.m - self.g
        return temp_vector

    def trajectory(self):
        """
        Computes the trajectory using all available data
        @return: time, postion, velocity
        @rtype: List: float
        """
        t_span = [0, self.t_f]  # interval Variables'integració
        w_0 = [0, 0]  # valors inicials
        t_val = arange(0, self.t_f, self.dt)  # valors de temps

        solution = solve_ivp(self.f, t_span, w_0, t_eval=t_val)

        return solution.t, solution.y[0], solution.y[1]
