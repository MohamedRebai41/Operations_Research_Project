from PyQt5 import QtWidgets, uic
import sys
sys.path.append('..')
from Scheduling.model import schedule

tasks = []
resources = []
tasks_resources = []
priority=[]

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

class AddPriorityDialog(QtWidgets.QDialog):
    def __init__(self):
        super(AddPriorityDialog, self).__init__()
        uic.loadUi('./priorityForm.ui', self)
        self.button.setStyleSheet("background-color: #8c4669; color: white;")
        self.button.clicked.connect(self.accept)
        self.comboBox.addItems([task for task in tasks])
        self.comboBox2.addItems([task for task in tasks])

    def getPriority(self):
        task1 = self.comboBox.currentText()
        task2 = self.comboBox2.currentText()
        return task1, task2

class Window2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window2, self).__init__()
        uic.loadUi('./window2.ui', self)
        #set window title
        self.setWindowTitle("Scheduling")
        self.button2.clicked.connect(self.getResourses)
        self.button2.setStyleSheet("background-color: #8c4669; color: white;")
        self.button3.setStyleSheet("background-color: #8c4669; color: white;")
        self.button3.clicked.connect(self.open_dialog)
        self.button4.setStyleSheet("background-color: #8c4669; color: white;")
        self.button4.clicked.connect(self.clear)
        self.button5.setStyleSheet("background-color: #8c4669; color: white;")
        self.button5.clicked.connect(self.open_dialog_priority)
        self.button6.setStyleSheet("background-color: #8c4669; color: white;")
        self.button6.clicked.connect(self.clear2)
        self.calc.setStyleSheet("background-color: #8c4669; color: white;")
        self.calc.clicked.connect(self.calculate)
        self.table.setColumnCount(3)  
        self.hideWidgets()

    def hideWidgets(self):
        self.table.hide()
        self.label3.hide()
        self.button3.hide()
        self.button4.hide()
        self.table2.hide()
        self.button5.hide()
        self.button6.hide()
        self.label1.hide()
        self.calc.hide()

    def showWidgets(self):
        self.table.show()
        self.button3.show()
        self.button4.show()
        self.label3.show()
        self.table2.show()
        self.button5.show()
        self.button6.show()
        self.label1.show()
        self.calc.show()

    def clear(self):
        self.table.setRowCount(0)
        tasks_resources.clear()

    def clear2(self):
        self.table2.setRowCount(0)
        priority.clear()
        
    def open_dialog_priority(self):
        dialog = AddPriorityDialog()
        dialog.setWindowTitle("Priority")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            task1, task2 = dialog.getPriority()
            if task1 and task2:
                row_position = self.table2.rowCount()
                self.table2.insertRow(row_position)
                self.table2.setItem(row_position, 0, QtWidgets.QTableWidgetItem(task1))
                self.table2.setItem(row_position, 1, QtWidgets.QTableWidgetItem(task2))
                delete_button = QtWidgets.QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_row2(row, task1, task2))
                self.table2.setCellWidget(row_position, 2, delete_button)
                priority.append((tasks.index(task1), tasks.index(task2)))
                print(priority)

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
        dialog.setWindowTitle("Tasks and Resources")
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
                print(tasks_resources)

    def delete_row(self, row, task, resource):
        self.table.removeRow(row)
        tasks_resources[tasks.index(task)].remove(resources.index(resource))
        print(tasks_resources)

    def delete_row2(self, row, task1, task2):
        self.table2.removeRow(row)
        priority.remove((tasks.index(task1), tasks.index(task2)))
        print(priority)

    def showInputWidgets(self):
        self.showWidgets()

    def calculate(self):
        try:
            result = schedule(len(tasks), len(resources), tasks_resources, priority)
            # self.resultTable.show()
            # self.resultTable.setRowCount(len(tasks))
            # for i, task in enumerate(tasks):
            #     resource_text = ', '.join([result[index] for index in tasks_resources[i]])
            #     self.resTable.setItem(i, 0, QtWidgets.QTableWidgetItem(task))
            #     self.resTable.setItem(i, 1, QtWidgets.QTableWidgetItem(resource_text))
            # self.resTable.resizeColumnsToContents()
            print(result)
        except Exception as e:
            print(e)
            

       


