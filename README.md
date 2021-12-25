# Python GUI for Rocket Simulations
 I made a GUI for rocket simulations for a school project. 
 It's only a basic GUI which given some inputs, predicts what a rocket might do in those circumstances. 
 It's coded in python as it is my main Programming Language and uses tkinter for the GUI.

This is one of my weekend projects so there's not a lot of effort putted into it, but i think it ended up great!

In the dist folder, there's the exe if you want to try it

**Versions:**
> 
> **Python 3.9.5**

The calculations code was made by Jordi Vasquez and its original code is on the source code. (Programa.py)

### Build:
Exectute the Build.ps1 file, which will automatically install all needed dependencies
```
.\build.ps1
```
#### Or:
Execute pyinstaller including the icon image:
```
python -m PyInstaller --onefile --windowed --icon={PATH}\Assets\Icon.ico Coet.py
```

***You must Include Defaults.JSON in the same directory as your .exe file***
