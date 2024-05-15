from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QTableWidget, QTableWidgetItem, QWidget, QDateEdit
from PyQt5.QtCore import QDate

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 500, 800, 400)  
        self.setWindowTitle("Task Tracker")
        self.initUI()

    def initUI(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)  

       
        inputLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

       
        self.taskInput = QLineEdit(self)
        self.taskInput.setPlaceholderText("Enter task name")
        self.descInput = QLineEdit(self)
        self.descInput.setPlaceholderText("Enter task description")
        self.deadlineInput = QDateEdit(self)
        self.deadlineInput.setDate(QDate.currentDate())
        self.deadlineInput.setCalendarPopup(True)
        inputLayout.addWidget(self.taskInput)
        inputLayout.addWidget(self.descInput)
        inputLayout.addWidget(self.deadlineInput)
        
      
        mainLayout.addLayout(inputLayout)

       
        self.addButton = QPushButton("Add", self)
        self.addButton.clicked.connect(self.addTask)
        self.removeButton = QPushButton("Remove", self)
        self.removeButton.clicked.connect(self.removeTask)
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.removeButton)
        
       
        mainLayout.addLayout(buttonLayout)

        self.taskTable = QTableWidget(self)
        self.taskTable.setRowCount(0)
        self.taskTable.setColumnCount(3)
        self.taskTable.setHorizontalHeaderLabels(["Task", "Description", "Deadline"])
        mainLayout.addWidget(self.taskTable)

    def addTask(self):
        task_name = self.taskInput.text()
        task_desc = self.descInput.text()
        deadline = self.deadlineInput.date().toString("yyyy-MM-dd")
        if task_name: 
            row_position = self.taskTable.rowCount()
            self.taskTable.insertRow(row_position)
            self.taskTable.setItem(row_position, 0, QTableWidgetItem(task_name))
            self.taskTable.setItem(row_position, 1, QTableWidgetItem(task_desc))
            self.taskTable.setItem(row_position, 2, QTableWidgetItem(deadline))

            self.taskInput.clear()
            self.descInput.clear()

    def removeTask(self):
        table_current_row = self.taskTable.currentRow()
        if table_current_row != -1:
            self.taskTable.removeRow(table_current_row)

if __name__ == "__main__":
    app = QApplication([])
    win = MyWindow()
    win.show()
    app.exec_()
