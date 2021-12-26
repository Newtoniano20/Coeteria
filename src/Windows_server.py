import os
import base64
from .Logo import img


def set_icon(tk):  # todo : Aquesta funció s'ha de cambiar
    with open(f"tmp_icon.ico", "wb+") as tmp2:
        tmp2.write(base64.b64decode(img))
        tmp2.close()
        tk.iconbitmap(f"tmp_icon.ico")
        os.remove(f"tmp_icon.ico")

