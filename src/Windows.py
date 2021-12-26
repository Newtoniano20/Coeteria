from .Windows_server import set_icon
from tkinter import Tk, Label
import matplotlib.pyplot as plt

BACKGROUND_COLOR = "#d4fffa"


def flight_info(y: list, v_y: list, t: list):
    max_vel = max(v_y)  # Maxima velocitat
    ap = max(y)  # Maxima altura
    s = fallv = tempsc = 0
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
    info_w.configure(bg=BACKGROUND_COLOR)

    # Printing out all the info:
    list_titles = [f"Apogeu: \n {ap} m", f"Màxima velocitat: \n {max_vel} m/s",
                   f"Velocitat d'aterratge: \n {fallv} m/s", f"Temps total del vol: \n {tempsc} s"]

    for i2 in range(len(list_titles)):
        text_printed = Label(info_w, text=list_titles[i2], bg=BACKGROUND_COLOR)
        text_printed.grid(row=1 + i2 * 2, column=3)
        Label(info_w, text="", bg=BACKGROUND_COLOR).grid(row=(2 + i2 * 2), column=0)


def graph(figure: int, x: list, y: list, cleaning: int, title: str, label: list, axis: list):
    plt.figure(figure)
    if cleaning == 1:
        plt.cla()
    plt.plot(x, y, 'r')
    plt.title(title)
    plt.xlabel(label[0])
    plt.ylabel(label[1])
    plt.axis(axis)
    plt.grid(True)
    plt.show()
