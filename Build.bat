@ECHO OFF
TITLE "PyInstaller - main.py"
rmdir /s /q Build

pyinstaller --workpath=.\Temp ^
	--specpath=.\Temp ^
	--distpath=.\Build ^
	--name "Program" ^
	--onefile main.py

rmdir /s /q __pycache__
rmdir /s /q Temp

