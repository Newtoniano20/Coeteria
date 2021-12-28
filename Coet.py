from tkinter import *
from PIL import ImageTk, Image
import base64
import os
from src import *
from tkinter.font import Font
from json import load

# Constants:
with open('Defaults.JSON') as f:
    forces = Forces(load(f))

BACKGROUND_COLOR = "#d4fffa"

root = Tk()
root.geometry("1000x700")
root.title("Taller Coeteria 2021")
with open("background.png", "wb+") as tmp:
    tmp.write(base64.b64decode(bkg_img))
background_image = ImageTk.PhotoImage(Image.open("background.png"))
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0)
os.remove("background.png")

set_icon(root)
title_font = Font(family="Helvetica", size=24, weight="bold")
Label(root, text="Taller de Coeteria", bg=BACKGROUND_COLOR, font=title_font).grid(row=0, column=2)
Label(root, text="Proxima Space Program\n", bg=BACKGROUND_COLOR, font=title_font).grid(row=1, column=2)
Label(root, text="", bg=BACKGROUND_COLOR).grid(row=2, column=1)

Parametres = ["Acceleració de la gravetat [m/s^2]: ", "Densitat al nivell del mar [kg/m^3]: ",
              "Escala de l'alçada [m]: ", "Coeficient del drag del coet [-]: ", "Àrea frontal del coet [m^2]:",
              'Massa "molla" del coet (inclou propel·lent) [kg]:',
              'Massa "seca" del coet (no inclou propel·lent) [kg]:', 'Thrust mitjà del coet [N]:',
              'Temps de cremat [s]:']
# todo : reformat this
Variables_Perametres = [forces.g, forces.rho_0, forces.H, forces.c_D, forces.A, forces.m_i, forces.m_f, forces.T_avg, forces.t_burn]
Variables = [forces.g, forces.rho_0, forces.H, forces.c_D, forces.A, forces.m_i, forces.m_f, forces.T_avg, forces.t_burn]

for i in range(len(Parametres)):
    Label(root, text=Parametres[i], bg=BACKGROUND_COLOR).grid(row=3 + i * 2, column=1)
    Variables[i] = Entry(root, width=50, borderwidth=1)  # input
    Variables[i].insert(0, Variables_Perametres[i])
    Variables[i].grid(row=3 + i * 2, column=2)
    Label(root, text="", bg=BACKGROUND_COLOR).grid(row=4 + i * 2, column=1)

Clean = IntVar()  # Variable integer de la casella Natejar el grafic
Checkbutton(root, text="Netejar el Gràfic", variable=Clean, bg=BACKGROUND_COLOR).grid(row=21, column=2)


def program(button_clicked):
    forces.update_variables(Variables)
    cleaning = Clean.get()  # Si la casella de neteja del grafic esta marcada o no (si = 1/ No =0)
    t, y, v_y = forces.trajectory()

    if button_clicked == 0:  # Informació del vol:
        flight_info(y, v_y, t)
    elif button_clicked == 1:  # Grafic Posició-Temps
        graph(figure=1, x=t, y=y, cleaning=cleaning, title="Trajectory", label=["$t$ [s]", "altitude [m]"], axis=[0, 100, 0, 11000])

    elif button_clicked == 2:  # Grafic Velocitat-Temps
        graph(figure=2, x=t, y=v_y, cleaning=cleaning, title="Velocity", label=["$t$ [s]", "velocity [m/s]"], axis=[0, 100, -300, 750])


Label(root, text="", bg=BACKGROUND_COLOR).grid(row=80, column=1)
# Botó trajectoria
Button(root, text="Gràfic Trajectòria", padx=35, pady=10, command=lambda: program(1), fg="white", bg="green").grid(row=85, column=1)

# Botó velocitat
Button(root, text="Gràfic Velocitat", padx=35, pady=10, command=lambda: program(2), fg="white", bg="green").grid(row=85, column=2)

# Botó Informació
Button(root, text="Informació del vol", padx=35, pady=10, command=lambda: program(0), fg="white", bg="green").grid(row=85, column=3)

root.mainloop()
