py -m pip install --upgrade pip
pip install pyinstaller
$PATH = [System.Environment]::CurrentDirectory
python -m PyInstaller --onefile --windowed --icon=$PATH\Assets\Icon.ico Coet.py