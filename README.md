# The App
## Description
This is the 2.0 version of my [Student Management System](https://github.com/YasirAtiq/Student_Management_System) app
## How to run the program
Run using:
```
python main.py
python3 main.py
python3.11 main.py
```

## How to make this a standalone app (.exe)
```
pip install pyinstaller
git clone https://github.com/YasirAtiq/Student_Management_System.git student_management_system
cd ./student_management_system
pyinstaller --onefile main.py
pyinstaller main.spec
```
**Now the main.exe file is in the dist directory**


## Dependencies: 
- mysql-connector-python==8.0.32
- protobuf==3.20.3
- PyQt6==6.5.3
- PyQt6-Qt6==6.5.3
- PyQt6-sip==13.6.0
