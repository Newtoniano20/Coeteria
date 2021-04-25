import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from qq import img #Import base64 format img
import qq2 #Import base64 format img
import base64, os
import tkinter.font as tkFont

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

background_color = "#d4fffa"
window = 0

root = tk.Tk()
root.geometry("1000x700")
root.title("Taller Coeteria 2021")
tmp2 = open("tmp.png","wb+")  
tmp2.write(base64.b64decode(qq2.img))
tmp2.close()
background_image = ImageTk.PhotoImage(Image.open("tmp.png"))
background_Label = tk.Label(root, image=background_image)
background_Label.place(x=0, y=0)
os.remove("tmp.png")

#background_image= ImageTk.PhotoImage(Image.open("12.png"))
#background_tk.Label = tk.Label(root, image=background_image)
#background_tk.Label.place(x=-20, y=-20)
def setIcon():
        tmp = open("tmp.ico","wb+")  
        tmp.write(base64.b64decode(img))
        tmp.close()
        root.iconbitmap("tmp.ico")
        os.remove("tmp.ico")
try:
    setIcon()
except:
    pass

Clean = tk.IntVar()

c = tk.Checkbutton(root, text= "Natejar el Grafic", variable=Clean, bg=background_color)

title = tkFont.Font(family="Helvetica",size=24,weight="bold")
#tk.Label(root, text="").grid(row=4, column=1)
myLabel1 = tk.Label(root, text="Taller de Coeteria", bg=background_color, font=title)
myLabel2 = tk.Label(root, text="Proxima Space Program\n", bg=background_color, font=title)
myLabel1.grid(row=0, column=2)
myLabel2.grid(row=1, column=2)

tk.Label(root, text="", bg=background_color).grid(row=2, column=1)

gravity = tk.Label(root, text = "Acceleració de la gravetat [m/s^2]: ", bg=background_color)
gravity.grid(row=3, column=1)
gv = tk.Entry(root, width=50, borderwidth=1) #input
gv.insert(0, g)
gv.grid(row=3, column=2)

tk.Label(root, text="", bg=background_color).grid(row=4, column=1)

Dens = tk.Label(root, text = "Densitat al nivell del mar [kg/m^3]: ", bg=background_color)
Dens.grid(row=5, column=1)
ds = tk.Entry(root, width=50, borderwidth=1) #input
ds.insert(0, rho_0)
ds.grid(row=5, column=2)

tk.Label(root, text="", bg=background_color).grid(row=6, column=1)

Escala = tk.Label(root, text = "Escala de l'alçada [m]: ", bg=background_color)
Escala.grid(row=7, column=1)
es = tk.Entry(root, width=50, borderwidth=1) #input
es.insert(0, H)
es.grid(row=7, column=2)

tk.Label(root, text="", bg=background_color).grid(row=8, column=1)

Escala = tk.Label(root, text = "Coeficient del drag del coet [-]: ", bg=background_color)
Escala.grid(row=9, column=1)
cdr = tk.Entry(root, width=50, borderwidth=1) #input
cdr.insert(0, c_D)
cdr.grid(row=9, column=2)

tk.Label(root, text="", bg=background_color).grid(row=10, column=1)

Area = tk.Label(root, text = "Àrea frontal del coet [m^2]:", bg=background_color)
Area.grid(row=11, column=1)
Ae = tk.Entry(root, width=50, borderwidth=1) #input
Ae.insert(0, A)
Ae.grid(row=11, column=2)

tk.Label(root, text="", bg=background_color).grid(row=12, column=1)

Molla = tk.Label(root, text = 'Massa "molla" del coet (inclou propel·lent) [kg]:', bg=background_color)
Molla.grid(row=13, column=1)
Mll = tk.Entry(root, width=50, borderwidth=1) #input
Mll.insert(0, m_i)
Mll.grid(row=13, column=2)

tk.Label(root, text="", bg=background_color).grid(row=14, column=1)

Seca = tk.Label(root, text = 'Massa "seca" del coet (no inclou propel·lent) [kg]:', bg=background_color)
Seca.grid(row=15, column=1)
Sc = tk.Entry(root, width=50, borderwidth=1) #input
Sc.insert(0, m_f)
Sc.grid(row=15, column=2)

tk.Label(root, text="", bg=background_color).grid(row=16, column=1)

Seca = tk.Label(root, text = 'Thrust mitjà del coet [N]:', bg=background_color)
Seca.grid(row=17, column=1)
Tm = tk.Entry(root, width=50, borderwidth=1) #input
Tm.insert(0, T_avg)
Tm.grid(row=17, column=2)

tk.Label(root, text="", bg=background_color).grid(row=18, column=1)

Seca = tk.Label(root, text = 'Temps de cremat [s]:', bg=background_color)
Seca.grid(row=19, column=1)
Th = tk.Entry(root, width=50, borderwidth=1) #input
Th.insert(0, t_burn)
Th.grid(row=19, column=2)

tk.Label(root, text="", bg=background_color).grid(row=20, column=1)

c.grid(row=21, column=2)

def Programa(w): 
    g = float(gv.get())         # acceleració de la gravetat [m/s^2]
    rho_0 = float(ds.get())     # Densitat al nivell del mar [kg/m^3]
    H = float(es.get())         # Escala de l'alçada [m]
    c_D =  float(cdr.get())     # Coeficient del drag del coet [-]
    A = float(Ae.get())         # Àrea frontal del coet [m^2]
    m_i = float(Mll.get())      # Massa "molla" del coet (inclou propel·lent) [kg]
    m_f = float(Sc.get())       # Massa "seca" del coet (no inclou propel·lent) [kg]
    T_avg = float(Tm.get())     # Thrust mitjà del coet [N]
    t_burn = float(Th.get())    # Temps de cremat [s]
    m = (m_i + m_f)/2           # Massa mitjana del coet
    k = 0.5*c_D*A*rho_0         # Factor constant en l'equació del Drag
    cl = Clean.get()
    def Thrust(t):
        if t < t_burn:
            return T_avg
        return 0

    def Drag(h, v):
        if v == 0: # Amb això ens estalviem dividir per 0.
            return 0
        return -k*np.exp(-h/H)*v*abs(v)

    def f(t, w):
        temp_vector = np.zeros(2)
        # Eq. (3) (1D)
        temp_vector[0] = w[1]
        # Eq. (4). In the 1D-case, r_y = r = h
        temp_vector[1] = (Thrust(t) + Drag(w[0],w[1]))/m - g
        return temp_vector

    def trajectory(dt, t_f):
        t_span = [0, t_f] # interval d'integració
        w_0 = [0, 0] # valors inicials
        t_val = np.arange(0, t_f, dt) # valors de temps
        
        solution = solve_ivp(f, t_span, w_0, t_eval=t_val)
        
        return solution.t, solution.y[0], solution.y[1]
    dt=0.02
    t_f=1200
    t, y, v_y = trajectory(dt,t_f)
    max_vel = max(v_y)
    ap = max(y)
    if w == 2:
        s = 0
        for n in y:
            s += 1
            if n < 0 and s != 1:
                fallv = v_y[s]
                tempsc = t[s]
                break
        info = tk.Tk()
        def setIcon():
            tmp = open("tmp.ico","wb+")  
            tmp.write(base64.b64decode(img))
            tmp.close()
            info.iconbitmap("tmp.ico")
            os.remove("tmp.ico")
        try:
            setIcon()
        except:
            pass
        info.geometry("300x200")
        info.title("Informació del vol:")
        info.configure(bg=background_color)
        Apog = tk.Label(info, text = f"Apogeu: \n {ap} m", bg=background_color)
        Apog.grid(row=1, column=3)
        tk.Label(root, text="", bg=background_color).grid(row=2, column=0)
        maxi = tk.Label(info, text = f"Màxima velocitat: \n {max_vel} m/s", bg=background_color)
        maxi.grid(row=3, column=3)
        tk.Label(root, text="", bg=background_color).grid(row=4, column=0)
        fall = tk.Label(info, text = f"Velocitat d'aterratge: \n {fallv} m/s", bg=background_color)
        fall.grid(row=5, column=3)
        tk.Label(root, text="", bg=background_color).grid(row=6, column=0)
        temps = tk.Label(info, text = f"Temps total del vol: \n {tempsc} s", bg=background_color)
        temps.grid(row=7, column=3)

    elif w == 0:
        plt.figure(1)
        if cl == 1:
            plt.cla()
        plt.plot(t,y,'r')
        plt.title("Trajectory")
        plt.xlabel("$t$ [s]")
        plt.ylabel("altitude [m]")
        plt.axis([0, 100, 0, 11000])
        plt.grid(True)
        plt.show()
        
    elif w== 1:
        plt.figure(2)
        if cl == 1:
            plt.cla()
        plt.plot(t,v_y,'r')
        plt.title("Velocity")
        plt.xlabel("$t$ [s]")
        plt.ylabel("velocity [m/s]")
        plt.axis([0, 100, -300, 750])
        plt.grid(True)
        plt.show()
    
def Traj():
    Programa(0)
def Vel():
    Programa(1)
def info():
    Programa(2)

#tk.Label(root, text="").grid(row=20, column=1)
#tk.Label(root, text="").grid(row=21, column=1)


#mytk.Button = tk.Button(root, text="Clean Graph", padx=20, pady=5, command=Vel, fg="white", bg="yellow")

#mytk.Button.grid(row=23, column=2)

tk.Label(root, text="", bg=background_color).grid(row=80, column=1)

Trajectoria = tk.Button(root, text="Grafic Trajectoria", padx=30, pady=10, command=Traj, fg="white", bg="green")

Trajectoria.grid(row=85, column=1)


Velocitat = tk.Button(root, text="Grafic Velocitat", padx=35, pady=10, command=Vel, fg="white", bg="green")

Velocitat.grid(row=85, column=2)


Information = tk.Button(root, text="Informació del vol", padx=35, pady=10, command=info, fg="white", bg="green")

Information.grid(row=85, column=3)


root.mainloop()