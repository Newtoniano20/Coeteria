from tkinter import *
from PIL import ImageTk, Image
from matplotlib.pyplot import plot, xlabel, ylabel, axis, grid, show, cla, figure
from matplotlib.pyplot import title as pltitle
import base64
import os
from src import *
from tkinter.font import Font
from json import load

# Constants:
with open('Defaults.JSON') as f:
    Defaults = load(f)

forces = Forces(Defaults)
background_color = "#d4fffa"

root = Tk()
root.geometry("1000x700")
root.title("Taller Coeteria 2021")
tmp2 = open("background.png", "wb+")
tmp2.write(base64.b64decode(bkg_img))
tmp2.close()
background_image = ImageTk.PhotoImage(Image.open("background.png"))
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0)
os.remove("background.png")


def set_icon(tk):  # todo : Aquesta funció s'ha de cambiar
    tmp = open(f"tmp_icon.ico", "wb+")
    tmp.write(base64.b64decode(logo_img))
    tmp.close()
    tk.iconbitmap(f"tmp_icon.ico")
    os.remove(f"tmp_icon.ico")


set_icon(root)

title = Font(family="Helvetica", size=24, weight="bold")
Titol = Label(root, text="Taller de Coeteria", bg=background_color, font=title)
Subtitol = Label(root, text="Proxima Space Program\n", bg=background_color, font=title)
Titol.grid(row=0, column=2)
Subtitol.grid(row=1, column=2)

Label(root, text="", bg=background_color).grid(row=2, column=1)

Parametres = ["Acceleració de la gravetat [m/s^2]: ", "Densitat al nivell del mar [kg/m^3]: ",
              "Escala de l'alçada [m]: ", "Coeficient del drag del coet [-]: ", "Àrea frontal del coet [m^2]:",
              'Massa "molla" del coet (inclou propel·lent) [kg]:',
              'Massa "seca" del coet (no inclou propel·lent) [kg]:', 'Thrust mitjà del coet [N]:',
              'Temps de cremat [s]:']
Variables_Perametres = [forces.g, forces.rho_0, forces.H, forces.c_D, forces.A, forces.m_i, forces.m_f, forces.T_avg, forces.t_burn]
Variables = [forces.g, forces.rho_0, forces.H, forces.c_D, forces.A, forces.m_i, forces.m_f, forces.T_avg, forces.t_burn]
varnum = 0

for Par in Parametres:
    Label(root, text=Par, bg=background_color).grid(row=3 + varnum * 2, column=1)
    Variables[varnum] = Entry(root, width=50, borderwidth=1)  # input
    Variables[varnum].insert(0, Variables_Perametres[varnum])
    Variables[varnum].grid(row=3 + varnum * 2, column=2)
    Label(root, text="", bg=background_color).grid(row=4 + varnum * 2, column=1)
    varnum += 1

Clean = IntVar()  # Variable integer de la casella Natejar el grafic
natejar_grafic = Checkbutton(root, text="Netejar el Gràfic", variable=Clean, bg=background_color)
natejar_grafic.grid(row=21, column=2)


def programa(button_clicked):
    forces.g = float(Variables[0].get())  # acceleració de la gravetat [m/s^2]
    forces.rho_0 = float(Variables[1].get())  # Densitat al nivell del mar [kg/m^3]
    forces.H = float(Variables[2].get())  # Escala de l'alçada [m]
    forces.c_D = float(Variables[3].get())  # Coeficient del drag del coet [-]
    forces.A = float(Variables[4].get())  # Àrea frontal del coet [m^2]
    forces.m_i = float(Variables[5].get())  # Massa "molla" del coet (inclou propel·lent) [kg]
    forces.m_f = float(Variables[6].get())  # Massa "seca" del coet (no inclou propel·lent) [kg]
    forces.T_avg = float(Variables[7].get())  # Thrust mitjà del coet [N]
    forces.t_burn = float(Variables[8].get())  # Temps de cremat [s]
    cleaning = Clean.get()  # Si la casella de neteja del grafic esta marcada o no (si = 1/ No =0)
    t, y, v_y = forces.trajectory()
    print("y: ", y)
    max_vel = max(v_y)  # Maxima velocitat
    ap = max(y)  # Maxima altura

    if button_clicked == 0:  # Informació del vol:
        s = 0
        fallv = 0
        tempsc = 0
        for n in y:
            s += 1
            if n < 0 and s != 1:
                fallv = v_y[s]
                tempsc = t[s]
                break
        info_w = Tk()
        set_icon(info_w)
        info_w.geometry("300x250")
        info_w.title("Informació del vol:")
        info_w.configure(bg=background_color)

        # Printing out all the info_w:
        list_titles = [f"Apogeu: \n {ap} m", f"Màxima velocitat: \n {max_vel} m/s",
                       f"Velocitat d'aterratge: \n {fallv} m/s", f"Temps total del vol: \n {tempsc} s"]
        iteration2 = 0

        for titles in list_titles:
            text_printed = Label(info_w, text=titles, bg=background_color)
            text_printed.grid(row=1 + iteration2 * 2, column=3)
            Label(info_w, text="", bg=background_color).grid(row=2 + iteration2 * 2, column=0)
            iteration2 += 1

    elif button_clicked == 1:  # Grafic Posició-Temps
        figure(1)
        if cleaning == 1:
            cla()
        plot(t, y, 'r')
        pltitle("Trajectory")
        xlabel("$t$ [s]")
        ylabel("altitude [m]")
        axis([0, 100, 0, 11000])
        grid(True)
        show()

    elif button_clicked == 2:  # Grafic Velocitat-Temps
        figure(2)
        if cleaning == 1:
            cla()
        plot(t, v_y, 'r')
        pltitle("Velocity")
        xlabel("$t$ [s]")
        ylabel("velocity [m/s]")
        axis([0, 100, -300, 750])
        grid(True)
        show()


def info():
    programa(0)


def traj():
    programa(1)


def vel():
    programa(2)


Label(root, text="", bg=background_color).grid(row=80, column=1)
# Botó trajectoria
Button(root, text="Gràfic Trajectòria", padx=30, pady=10, command=traj, fg="white", bg="green").grid(row=85, column=1)

# Botó velocitat
Button(root, text="Gràfic Velocitat", padx=35, pady=10, command=vel, fg="white", bg="green").grid(row=85, column=2)

# Botó Informació
Button(root, text="Informació del vol", padx=35, pady=10, command=info, fg="white", bg="green").grid(row=85, column=3)

root.mainloop()
