from PyQt5 import QtWidgets, uic
import sys
import os
from PyQt5.QtWidgets import QMessageBox

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# from Nutrition.model import optimize
class AddItemDialog(QtWidgets.QDialog):
    def __init__(self):
        super(AddItemDialog, self).__init__()
        uic.loadUi('./itemForm.ui', self)  
        self.button.clicked.connect(self.accept)
        self.button.setStyleSheet("background-color: #8c4669; color: white;")

    def get_data(self):
        item = self.text1.toPlainText()
        proteine = self.text2.toPlainText()
        calories = self.text3.toPlainText()
        calcium = self.text4.toPlainText()
        cout = self.text5_1.toPlainText()
        return item, proteine, calories, calcium, cout

class AddConstraintDialog(QtWidgets.QDialog):
    def __init__(self):
        super(AddConstraintDialog, self).__init__()
        uic.loadUi('./constraintForm.ui', self)
        self.add0.clicked.connect(self.accept)
        self.add0.setStyleSheet("background-color: #8c4669; color: white;")

        #add all the items to the combobox from the list of items
        self.comboBox.addItems([item[0] for item in items])

    def get_data(self):
        constraint = self.comboBox.currentText()
        valeur = self.text2.toPlainText()
        if constraint and valeur:
            return constraint, valeur
        return None, None

items=[]
constraints=[]
proteines=0
calories=0
calcium=0

class Window1(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window1, self).__init__()
        uic.loadUi('./window1.ui', self)
        self.setWindowTitle("Nutrition")
        self.button1.clicked.connect(self.open_dialog)
        self.button1.setStyleSheet("background-color: #8c4669; color: white;")
        self.table1.setColumnCount(6)  
        self.table2.setColumnCount(3)
        self.add.clicked.connect(self.add_constraint)
        self.add.setStyleSheet("background-color: #8c4669; color: white;")
        self.opt.setStyleSheet("background-color: #8c4669; color: white;")
        self.opt.clicked.connect(self.optimise)
        self.add1.setStyleSheet("background-color: #8c4669; color: white;")
        self.add1.clicked.connect(self.getProteines)
        self.add2.setStyleSheet("background-color: #8c4669; color: white;")
        self.add2.clicked.connect(self.getCalories)
        self.add3.setStyleSheet("background-color: #8c4669; color: white;")
        self.add3.clicked.connect(self.getCalcium)

        self.result.hide()

    def getProteines(self):
        for i in range(len(constraints)):
            if constraints[i][0] == "proteines":
                return
        global proteines 
        proteines=self.cont1.toPlainText()
        if proteines:
            if proteines.isdigit():
                constraints.append(["proteines", proteines])
                row_position = self.table2.rowCount()
                self.table2.insertRow(row_position)
                self.table2.setItem(row_position, 0, QtWidgets.QTableWidgetItem("proteines"))
                self.table2.setItem(row_position, 1, QtWidgets.QTableWidgetItem(proteines))
                delete_button = QtWidgets.QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_row2(row))
                self.table2.setCellWidget(row_position, 2, delete_button)
            else :
                self.show_error_message("Please enter a valid input")
                return

    def getCalories(self):
        for i in range(len(constraints)):
            if constraints[i][0] == "calories":
                return
        global calories
        calories=self.cont2.toPlainText()
        if calories :
            if calories.isdigit():
                constraints.append(["calories", calories])
                row_position = self.table2.rowCount()
                self.table2.insertRow(row_position)
                self.table2.setItem(row_position, 0, QtWidgets.QTableWidgetItem("calories"))
                self.table2.setItem(row_position, 1, QtWidgets.QTableWidgetItem(calories))
                delete_button = QtWidgets.QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_row2(row))
                self.table2.setCellWidget(row_position, 2, delete_button)
            else :
                self.show_error_message("Please enter a valid input")
                return

        
    def getCalcium(self):
        for i in range(len(constraints)):
            if constraints[i][0] == "calcium":
                return
        global calcium
        calcium=self.cont3.toPlainText()
        if calcium:
            if calcium.isdigit():
                constraints.append(["calcium", calcium])
                row_position = self.table2.rowCount()
                self.table2.insertRow(row_position)
                self.table2.setItem(row_position, 0, QtWidgets.QTableWidgetItem("calcium"))
                self.table2.setItem(row_position, 1, QtWidgets.QTableWidgetItem(calcium))
                delete_button = QtWidgets.QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_row2(row))
                self.table2.setCellWidget(row_position, 2, delete_button)
            else :
                self.show_error_message("Please enter a valid input")
                return


    def open_dialog(self):
        dialog = AddItemDialog()
        dialog.setWindowTitle("Add Element")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            item, proteine, calories, calcium, cout = dialog.get_data()

            if item and proteine and calories and calcium and cout:
                if not proteine.isdigit() or not calories.isdigit() or not calcium.isdigit() or not cout.isdigit() or not item.isalpha():
                    self.show_error_message("Please enter a valid input")
                    return
                row_position = self.table1.rowCount()
                self.table1.insertRow(row_position)

                self.table1.setItem(row_position, 0, QtWidgets.QTableWidgetItem(item))
                self.table1.setItem(row_position, 1, QtWidgets.QTableWidgetItem(proteine))
                self.table1.setItem(row_position, 2, QtWidgets.QTableWidgetItem(calories))
                self.table1.setItem(row_position, 3, QtWidgets.QTableWidgetItem(calcium))
                self.table1.setItem(row_position, 4, QtWidgets.QTableWidgetItem(cout))

                delete_button = QtWidgets.QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_row1(row))
                self.table1.setCellWidget(row_position, 5, delete_button)  
                items.append([item, proteine, calories, calcium, cout])
                print(items)

            else :
                self.show_error_message("Please fill all the fields")
                return

    def add_constraint(self):
        dialog = AddConstraintDialog()
        dialog.setWindowTitle("Add Constraint")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            constraint, valeur = dialog.get_data()

            if constraint and valeur:
                if not valeur.isdigit():
                    self.show_error_message("Please enter a valid input")
                    return
                row_position = self.table2.rowCount()
                self.table2.insertRow(row_position)

                self.table2.setItem(row_position, 0, QtWidgets.QTableWidgetItem(constraint))
                self.table2.setItem(row_position, 1, QtWidgets.QTableWidgetItem(valeur))

                delete_button = QtWidgets.QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_row2(row))
                self.table2.setCellWidget(row_position, 2, delete_button)
                constraints.append([constraint, valeur])
                print(constraints)
            
            else :
                self.show_error_message("Please fill all the fields")
                return

    def delete_row1(self, row):
        #delete the constraints
        for i in range(len(constraints)):
            if constraints[i][0] == items[row][0]:
                constraints.pop(i)
                self.table2.removeRow(i)
                break
        self.table1.removeRow(row)
        items.pop(row)
    
    def delete_row2(self, row):
        self.table2.removeRow(row)
        constraints.pop(row)

    def optimise(self):
        print("Optimising...")
        if items and constraints:
            if proteines and calories and calcium:
                nb_items = len(items)
                names = [item[0] for item in items]
                cout = [int(item[4]) for item in items]
                constraintsInf= []
                constraintsSup = []
                self.result.show()

                #     for i in range(len(constraints)):
                #         temp = [0]*nb_items
                #         for j in range(nb_items):
                #             if constraints[i][0] == names[j]:
                #                 temp[j] = 1
                #                 break
                #         temp.append(int(constraints[i][1]))
                #         constraintsSup.append(temp)
                #     const = [proteines, calories, calcium]
                #     for i in range(3):
                #         temp = []
                #         for j in range(nb_items):
                #             temp.append(items[j][i+1])
                #         temp.append(int(const[i]))
                #         constraintsInf.append(temp)
                #     # call the optimization function to get the result 
                #     x=optimize(nb_items, names, cout, constraintsInf, constraintsSup)
                #     # Clear existing table content
                #     self.result.clearContents()
                #     print(x)

                #     # # Set row and column count
                # self.result.setRowCount(len(items))

                # for i in range(nb_items):
                #     self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(str(items[i][0])))
                #     self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(str(x[i])))
                # print("Optimisation done")
            else:
                self.show_error_message("You need to add the basic constraints")
                return

    def show_error_message(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

       



