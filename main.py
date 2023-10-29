from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit, 
                             QPushButton, QMainWindow, QTableWidget, 
                             QTableWidgetItem, QDialog, QVBoxLayout, 
                             QComboBox, QToolBar, QStatusBar, QMessageBox)
from PyQt6.QtGui import QAction, QIcon
import sqlite3
import sys

connection = sqlite3.connect("database.db")
raw_course = list(connection.execute("SELECT * FROM Courses"))
courses = []
for i in raw_course:
    course = i[1]
    courses.append(course)
connection.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Register Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        search_student_action = QAction("Find Student", self)
        search_student_action.triggered.connect(self.search)
        add_student_action.setMenuRole(QAction.MenuRole.NoRole)
        edit_menu_item.addAction(search_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course",
                                              "Phone no."))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        add_student_toolbar_action = toolbar.addAction(
            QIcon("icons//add.png"), "Register Student")
        add_student_toolbar_action.triggered.connect(
            add_student_action.trigger)

        add_student_toolbar_action = toolbar.addAction(
            QIcon("icons//search.png"), "Search Student")
        add_student_toolbar_action.triggered.connect(
            search_student_action.trigger)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.hide()

        self.table.cellClicked.connect(self.cell_clicked)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = list(connection.execute("SELECT * FROM students"))
        self.table.setRowCount(0)
        for index, row in enumerate(result):
            self.table.insertRow(index)
            for col_num, data in enumerate(row):
                self.table.setItem(index, col_num,
                                   QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog(self.table)
        dialog.exec()

    def edit(self):
        dialog = EditRecord(self.table)
        dialog.exec()

    def remove(self):
        dialog = RemoveRecord(self.table)
        dialog.exec()

    def about(self):
        dialog = AboutPage()
        dialog.exec()

    def cell_clicked(self):
        self.status_bar.show()
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.remove)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Details")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.courses_dropbox = QComboBox()
        self.courses_dropbox.addItems(courses)
        layout.addWidget(self.courses_dropbox)

        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone no.")
        layout.addWidget(self.phone_number)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.add_student)
        layout.addWidget(register_button)

        self.output = QLabel("")
        layout.addWidget(self.output)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.courses_dropbox.itemText(
            self.courses_dropbox.currentIndex())
        phone_number = self.phone_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
            (name, course, phone_number))
        self.output.setText("Inserted student details successfully.")
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.setWindowTitle("Insert Student Details")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Name of Student")
        layout.addWidget(self.search_name)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        self.output = QLabel("")
        layout.addWidget(self.output)

        self.setLayout(layout)

    def search(self):
        name = self.search_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?",
                                (name,))
        rows = list(result)
        items = self.table.findItems(name,
                                     Qt.MatchFlag.MatchFixedString)

        for item in items:
            self.table.item(item.row(), 0).setSelected(True)
            self.table.item(item.row(), 1).setSelected(True)
            self.table.item(item.row(), 2).setSelected(True)
            self.table.item(item.row(), 3).setSelected(True)
            self.output.setText("Please close this window.")
        cursor.close()
        connection.close()


class EditRecord(QDialog):
    def __init__(self, table: QTableWidget):
        super().__init__()
        self.table = table
        self.setWindowTitle("Edit Student Details")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = self.table.currentRow()
        student_name = self.table.item(index, 1).text()
        phone_number = self.table.item(index, 3).text()
        course_name = self.table.item(index, 2).text()
        self.id = self.table.item(index, 0).text()
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.courses_dropbox = QComboBox()
        self.courses_dropbox.addItems(courses)
        self.courses_dropbox.setCurrentText(course_name)
        layout.addWidget(self.courses_dropbox)

        self.phone_number = QLineEdit(phone_number)
        self.phone_number.setPlaceholderText("Phone no.")
        layout.addWidget(self.phone_number)

        register_button = QPushButton("Update")
        register_button.clicked.connect(self.edit_record)
        layout.addWidget(register_button)

        self.output = QLabel("")
        layout.addWidget(self.output)

        self.setLayout(layout)

    def edit_record(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET name = ?, course = ?, mobile = ? "
            "WHERE id = ?", (self.student_name.text(),
                             self.courses_dropbox.itemText(
                                 self.courses_dropbox.currentIndex()),
                             self.phone_number.text(), self.id))
        self.output.setText("Updated details successfully.")
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class RemoveRecord(QDialog):
    def __init__(self, table: QTableWidget):
        super().__init__()
        self.table = table
        self.setWindowTitle("Delete Student Details")
        layout = QGridLayout()

        confirmation = QLabel(
            "Are you sure you want to remove student details?")
        layout.addWidget(confirmation, 0, 0, 1, 2)

        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self.delete_record)
        layout.addWidget(yes_button, 1, 0)

        no_button = QPushButton("No")
        no_button.clicked.connect(self.reject)
        layout.addWidget(no_button, 1, 1)

        self.setLayout(layout)

    def delete_record(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        index = self.table.currentRow()
        id = self.table.item(index, 0).text()
        cursor.execute("DELETE FROM students WHERE id=?", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.reject()


class AboutPage(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Me")
        content = """
        Hello! My name is Yasir Atiq and I am Ardit Sulce's(the teachr) student.
        I am currently doing his course "Python Mega Course: Learn Python in 60 Days, Build 20 Apps"
        This is his app number 13. """
        self.setText(content)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
