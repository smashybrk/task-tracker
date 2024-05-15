import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QPushButton, QLineEdit


class ViewAllTasksWindow(QMainWindow):
    def __init__(self, cursor, parent=None):
        super(ViewAllTasksWindow, self).__init__(parent)
        self.setGeometry(200, 200, 600, 400)
        self.setWindowTitle("All Tasks")
        self.cursor = cursor
        self.initUI()

    def initUI(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)

        self.taskTable = QTableWidget(self)
        mainLayout.addWidget(self.taskTable)

        buttonLayout = QHBoxLayout()

        self.addTaskButton = QPushButton("Add Task", self)
        self.addTaskButton.clicked.connect(self.addTask)
        buttonLayout.addWidget(self.addTaskButton)

        self.removeTaskButton = QPushButton("Remove Task", self)
        self.removeTaskButton.clicked.connect(self.removeTask)
        buttonLayout.addWidget(self.removeTaskButton)

        mainLayout.addLayout(buttonLayout)

        self.displayTasks()

    def displayTasks(self):
        self.taskTable.clear()
        self.taskTable.setColumnCount(3)
        self.taskTable.setHorizontalHeaderLabels(["Task", "Description", "Deadline"])

        self.cursor.execute('''SELECT * FROM tasks''')
        tasks = self.cursor.fetchall()
        self.taskTable.setRowCount(len(tasks))

        for i, task in enumerate(tasks):
            for j, item in enumerate(task):
                self.taskTable.setItem(i, j, QTableWidgetItem(str(item)))

    def addTask(self):
        # Create a window to add a task
        add_task_window = AddTaskWindow(self.cursor)
        add_task_window.exec_()
        # Refresh the task list after adding a task
        self.displayTasks()

    def removeTask(self):
        # Get the selected row index
        selected_row = self.taskTable.currentRow()
        if selected_row != -1:
            # Get the task ID from the first column of the selected row
            task_id = self.taskTable.item(selected_row, 0).text()
            # Remove the task with the selected ID from the database
            self.cursor.execute('''DELETE FROM tasks WHERE id = ?''', (task_id,))
            self.cursor.connection.commit()
            # Refresh the task list after removing a task
            self.displayTasks()


class AddTaskWindow(QtWidgets.QDialog):
    def __init__(self, cursor, parent=None):
        super(AddTaskWindow, self).__init__(parent)
        self.setWindowTitle("Add Task")
        self.cursor = cursor
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText("Task name")
        layout.addWidget(self.taskInput)

        self.descInput = QLineEdit()
        self.descInput.setPlaceholderText("Task description")
        layout.addWidget(self.descInput)

        self.deadlineInput = QLineEdit()
        self.deadlineInput.setPlaceholderText("Deadline (YYYY-MM-DD)")
        layout.addWidget(self.deadlineInput)

        addButton = QPushButton("Add Task")
        addButton.clicked.connect(self.addTask)
        layout.addWidget(addButton)

        self.setLayout(layout)

    def addTask(self):
        task_name = self.taskInput.text()
        task_desc = self.descInput.text()
        deadline = self.deadlineInput.text()
        if task_name and deadline:
            self.cursor.execute('''INSERT INTO tasks (name, description, deadline) VALUES (?, ?, ?)''',
                                (task_name, task_desc, deadline))
            self.cursor.connection.commit()
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    view_all_tasks_window = ViewAllTasksWindow(cursor)
    view_all_tasks_window.show()
    app.exec_()
