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

    def thrust(self, t):
        if t < self.t_burn:
            return self.T_avg
        return 0

    def drag(self, h, v):
        if v == 0:  # Amb això ens estalviem dividir per 0.
            return 0
        return -self.k * exp(-h / self.H) * v * abs(v)

    def paracaigudes(self, v, t):
        pass

    def f(self, t, w):
        temp_vector = zeros(2)
        # Eq. (3) (1D)
        temp_vector[0] = w[1]
        # Eq. (4). In the 1D-case, r_y = r = h
        temp_vector[1] = (self.thrust(t) + self.drag(w[0], w[1])) / self.m - self.g
        return temp_vector

    def trajectory(self):
        t_span = [0, self.t_f]  # interval Variables'integració
        w_0 = [0, 0]  # valors inicials
        t_val = arange(0, self.t_f, self.dt)  # valors de temps

        solution = solve_ivp(self.f, t_span, w_0, t_eval=t_val)

        return solution.t, solution.y[0], solution.y[1]
