from tkinter import *
from PIL import ImageTk, Image
from numpy import zeros, exp, arange
from scipy.integrate import solve_ivp
from matplotlib.pyplot import plot, xlabel, ylabel, axis, grid, show, cla, figure
from matplotlib.pyplot import title as pltitle
import Logo                 #Logo in base 64
import background_image_64  #background image in base 64
import base64, os
from tkinter.font import Font
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

root = Tk()
root.geometry("1000x700")
root.title("Taller Coeteria 2021")
tmp2 = open("background.png","wb+")  
tmp2.write(base64.b64decode(background_image_64.img))
tmp2.close()
background_image = ImageTk.PhotoImage(Image.open("background.png"))
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0)
os.remove("background.png")


def setIcon(tk): #Aquesta funció s'ha de cambiar
        tmp = open(f"tmp_icon.ico","wb+")  
        tmp.write(base64.b64decode(Logo.img))
        tmp.close()
        tk.iconbitmap(f"tmp_icon.ico")
        os.remove(f"tmp_icon.ico")
setIcon(root)


title = Font(family="Helvetica",size=24,weight="bold")
Titol = Label(root, text="Taller de Coeteria", bg=background_color, font=title)
Subtitol = Label(root, text="Proxima Space Program\n", bg=background_color, font=title)
Titol.grid(row=0, column=2)
Subtitol.grid(row=1, column=2)

space = Label(root, text="", bg=background_color).grid(row=2, column=1)

Parametres = ["Acceleració de la gravetat [m/s^2]: ", "Densitat al nivell del mar [kg/m^3]: ","Escala de l'alçada [m]: ","Coeficient del drag del coet [-]: ","Àrea frontal del coet [m^2]:",'Massa "molla" del coet (inclou propel·lent) [kg]:','Massa "seca" del coet (no inclou propel·lent) [kg]:', 'Thrust mitjà del coet [N]:','Temps de cremat [s]:']
Variables_Perametres = [g, rho_0, H, c_D, A, m_i, m_f, T_avg,t_burn]
Variables = [g, rho_0, H, c_D, A, m_i, m_f, T_avg,t_burn]
varnum = 0

for Par in Parametres:
    TextLabel = Label(root, text = Par, bg=background_color).grid(row=3 + varnum*2, column=1)
    Variables[varnum] = Entry(root, width=50, borderwidth=1) #input
    Variables[varnum].insert(0, Variables_Perametres[varnum])
    Variables[varnum].grid(row=3 + varnum*2, column=2)
    space = Label(root, text="", bg=background_color).grid(row=4 + varnum*2, column=1)
    varnum += 1

Clean = IntVar() #Variable integer de la casella Natejar el grafic
natejar_grafic = Checkbutton(root, text= "Netejar el Gràfic", variable=Clean, bg=background_color)
natejar_grafic.grid(row=21, column=2)

def Programa(Button_Clicked): 
    g = float(Variables[0].get())         # acceleració de la gravetat [m/s^2]
    rho_0 = float(Variables[1].get())     # Densitat al nivell del mar [kg/m^3]
    H = float(Variables[2].get())         # Escala de l'alçada [m]
    c_D =  float(Variables[3].get())     # Coeficient del drag del coet [-]
    A = float(Variables[4].get())         # Àrea frontal del coet [m^2]
    m_i = float(Variables[5].get())      # Massa "molla" del coet (inclou propel·lent) [kg]
    m_f = float(Variables[6].get())       # Massa "seca" del coet (no inclou propel·lent) [kg]
    T_avg = float(Variables[7].get())     # Thrust mitjà del coet [N]
    t_burn = float(Variables[8].get())    # Temps de cremat [s]
    m = (m_i + m_f)/2                     # Massa mitjana del coet
    k = 0.5*c_D*A*rho_0                   # Factor constant en l'equació del Drag
    cleaning = Clean.get()                #Si la casella de neteja del grafic esta marcada o no (si = 1/ No =0)
    
    def Thrust(t):
        if t < t_burn:
            return T_avg
        return 0

    def Drag(h, v):
        if v == 0: # Amb això ens estalviem dividir per 0.
            return 0
        return -k*exp(-h/H)*v*abs(v)

    def Paracaigudes(v, t):
        pass
    def f(t, w):
        temp_vector = zeros(2)
        # Eq. (3) (1D)
        temp_vector[0] = w[1]
        # Eq. (4). In the 1D-case, r_y = r = h
        temp_vector[1] = (Thrust(t) + Drag(w[0],w[1]))/m - g
        return temp_vector

    def trajectory(dt, t_f):
        t_span = [0, t_f] # interval Variables'integració
        w_0 = [0, 0] # valors inicials
        t_val = arange(0, t_f, dt) # valors de temps
        
        solution = solve_ivp(f, t_span, w_0, t_eval=t_val)
        
        return solution.t, solution.y[0], solution.y[1]
    
    #Valors d'integració:
    dt=0.02
    t_f=1200

    t, y, v_y = trajectory(dt,t_f)
    max_vel = max(v_y) #Maxima velocitat
    ap = max(y) #Maxima altura
    
    if Button_Clicked == 0: #Informació del vol:
        s = 0
        for n in y:
            s += 1
            if n < 0 and s != 1:
                fallv = v_y[s]
                tempsc = t[s]
                break
        info = Tk()
        setIcon(info)
        info.geometry("300x250")
        info.title("Informació del vol:")
        info.configure(bg=background_color)

        #Printing out all the info:
        List_titles = [f"Apogeu: \n {ap} m", f"Màxima velocitat: \n {max_vel} m/s", f"Velocitat d'aterratge: \n {fallv} m/s", f"Temps total del vol: \n {tempsc} s"]
        iteration2 = 0

        for title in List_titles:
            Text_Printed = Label(info, text = title, bg=background_color)
            Text_Printed.grid(row=1 + iteration2*2, column=3)
            space = Label(info, text="", bg=background_color).grid(row=2+iteration2*2, column=0)
            iteration2 += 1
        
    elif Button_Clicked == 1: #Grafic Posició-Temps
        figure(1)
        if cleaning == 1:
            cla()
        plot(t,y,'r')
        pltitle("Trajectory")
        xlabel("$t$ [s]")
        ylabel("altitude [m]")
        axis([0, 100, 0, 11000])
        grid(True)
        show()
        
    elif Button_Clicked == 2: #Grafic Velocitat-Temps
        figure(2)
        if cleaning == 1:
            cla()
        plot(t,v_y,'r')
        pltitle("Velocity")
        xlabel("$t$ [s]")
        ylabel("velocity [m/s]")
        axis([0, 100, -300, 750])
        grid(True)
        show()

def info():
    Programa(0)
def Traj():
    Programa(1)
def Vel():
    Programa(2)

space = Label(root, text="", bg=background_color).grid(row=80, column=1)
#Botó trajectoria
Trajectoria = Button(root, text="Gràfic Trajectòria", padx=30, pady=10, command=Traj, fg="white", bg="green")

Trajectoria.grid(row=85, column=1)
#Botó velocitat
Velocitat = Button(root, text="Gràfic Velocitat", padx=35, pady=10, command=Vel, fg="white", bg="green")

Velocitat.grid(row=85, column=2)
#Botó Informació
Information = Button(root, text="Informació del vol", padx=35, pady=10, command=info, fg="white", bg="green")

Information.grid(row=85, column=3)

root.mainloop()