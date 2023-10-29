# The App
## Description
This app aims to build an app which will show a table with the student name, the course they are taking and their
mobile number. The user can also add, search, edit or delete this data.
## How to run the program
Run using:
- $ python main.py
- $ python3 main.py
- $ python3.11 main.py

## How to make this a standalone app (.exe)
- $ pyinstaller --onefile main.py
- Add:

data=[

(r'path\to\this\folder\database.db','.')
]

to the main.spec file at the end.
- $ pyinstaller main.spec
- Open dist\main.exe
- Overwrite the database.db with the database.db in the main folder.

## Dependencies: 
- altgraph==0.17.4 
- packaging==23.2 
- pefile==2023.2.7 
- pyinstaller==6.1.0 
- pyinstaller-hooks-contrib==2023.10 
- PyQt6==6.5.3 
- PyQt6-Qt6==6.5.3 
- PyQt6-sip==13.6.0 
- pywin32-ctypes==0.2.2