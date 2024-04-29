from PyQt5 import QtWidgets, uic

tasks = []
resources = []
tasks_resources = []

class AddTaskDialog(QtWidgets.QDialog):
    def __init__(self):
        super(AddTaskDialog, self).__init__()
        uic.loadUi('./taskForm.ui', self)
        self.button.setStyleSheet("background-color: #8c4669; color: white;")
        self.button.clicked.connect(self.accept)
        self.comboBox.addItems([task for task in tasks])
        self.comboBox2.addItems([resource for resource in resources])

    def getTasks(self):
        task = self.comboBox.currentText()
        resource = self.comboBox2.currentText()
        return task, resource


class Window2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window2, self).__init__()
        uic.loadUi('./window2.ui', self)
        self.button2.clicked.connect(self.getResourses)
        self.button2.setStyleSheet("background-color: #8c4669; color: white;")
        self.button3.setStyleSheet("background-color: #8c4669; color: white;")
        self.button3.clicked.connect(self.open_dialog)
        self.button4.setStyleSheet("background-color: #8c4669; color: white;")
        self.button4.clicked.connect(self.clear)
        self.table.setColumnCount(3)  
        self.hideWidgets()

    def hideWidgets(self):
        self.table.hide()
        self.label3.hide()
        self.button3.hide()
        self.button4.hide()

    def showWidgets(self):
        self.table.show()
        self.button3.show()
        self.button4.show()
        self.label3.show()

    def clear(self):
        self.table.setRowCount(0)
        tasks.clear()
        resources.clear()
        tasks_resources.clear()
        self.text1.clear()
        self.text2.clear()
        self.hideWidgets()

    def getResourses(self):
        res_num = self.text2.toPlainText()
        task_num = self.text1.toPlainText()
        if res_num and task_num :
            resources.clear()
            for i in range(int(res_num)):
                resources.append('Resource ' + str(i))
            tasks.clear()
            for i in range(int(task_num)):
                tasks.append('Task ' + str(i))
                tasks_resources.append([])
            self.showWidgets()

    def open_dialog(self):
        dialog = AddTaskDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            task, resource = dialog.getTasks()
            if task and resource:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(task))
                self.table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(resource))
                delete_button = QtWidgets.QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_row(row, task, resource))
                self.table.setCellWidget(row_position, 2, delete_button)
                tasks_resources[tasks.index(task)].append(resources.index(resource))

    def delete_row(self, row, task, resource):
        self.table.removeRow(row)
        tasks_resources[tasks.index(task)].remove(resources.index(resource))

    def showInputWidgets(self):
        self.showWidgets()

