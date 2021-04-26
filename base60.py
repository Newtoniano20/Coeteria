from tkinter import *
import base64

#Encoder to base 64
open_icon = open("12.png","rb") #qq.icon is the icon you want to put in
b64str = base64.b64encode(open_icon.read()) #Read in base64 format
open_icon.close()
write_data = "img=%s" % b64str
f = open("qq2.py","w+") #Write the data read above into the img array of qq.py
f.write(write_data)
