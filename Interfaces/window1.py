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
        # self.button.clicked.connect(self.accept)
        # self.button.setStyleSheet("background-color: #035283; color: white;")
        self.create_input_fields(numCont)

    def create_input_fields(self, numCont):
        # Create input field for element
        self.element_input = QtWidgets.QLineEdit(self)
        self.element_input.setObjectName('element')
        self.element_input.setPlaceholderText("Element")
        self.element_input.setGeometry(30, 30, 100, 30)

        # Create input fields for cont
        self.cont_inputs = []
        for i in range(numCont):
            input_field = QtWidgets.QTextEdit(self)
            input_field.setObjectName(contraintes[i])
            input_field.setPlaceholderText(contraintes[i])
            input_field.setGeometry(30 + (i+1)*110, 30 , 100, 30)
            self.cont_inputs.append(input_field)

        # Create input field for cout
        self.cout_input = QtWidgets.QLineEdit(self)
        self.cout_input.setObjectName('cout')
        self.cout_input.setPlaceholderText("Cout")
        self.cout_input.setGeometry(30 + (numCont+1)*110, 30 , 100, 30)

        #add button
        self.button = QtWidgets.QPushButton(self)
        self.button.setObjectName('button')
        self.button.setText('Ajouter')
        self.button.setGeometry(40 + (numCont+2)*110, 30, 100, 30)
        self.button.setStyleSheet("background-color: #035283; color: white;")
        self.button.clicked.connect(self.accept)

        #adjust window size
        self.setFixedSize(200 + (numCont+2)*110, 100)

    

    def get_data(self):
        element = self.element_input.text()
        cont = [input_field.toPlainText() for input_field in self.cont_inputs]
        cout = self.cout_input.text()
        return element, cont, cout

class AddElementContDialog(QtWidgets.QDialog):
    def __init__(self,str):
        super(AddElementContDialog, self).__init__()
        uic.loadUi('./constraintForm.ui', self)
        self.add0.clicked.connect(self.accept)
        self.add0.setStyleSheet("background-color: #035283; color: white;")
        if (str=='element'):
        #add all the items to the combobox from the list of items
            self.comboBox.addItems([element[0] for element in elements])
        else: 
            self.comboBox.addItems(contraintes)

    def get_data(self):
        constraint = self.comboBox.currentText()
        valeur = self.text2.toPlainText()
        if constraint and valeur:
            return constraint, valeur
        return None, None
#[apple, 2, 3, 4, 5]
elements=[]
#(proteines, 2)
objectifs=[]
#proteines,calsium, calories
contraintes=[]
#(apple, 2)
elementsCont=[]
numCont=0

class Window1(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window1, self).__init__()
        uic.loadUi('./window1.ui', self)
        self.setWindowTitle("Nutrition")
        self.add.clicked.connect(self.open_dialog)
        self.add.setStyleSheet("background-color: #035283; color: white;")
        self.addEl.clicked.connect(self.addElCont)
        self.addEl.setStyleSheet("background-color: #035283; color: white;")
        self.opt.setStyleSheet("background-color: #035283; color: white;")
        # self.opt.clicked.connect(self.optimise)
        self.addNum.setStyleSheet("background-color: #035283; color: white;")
        self.addNum.clicked.connect(self.numContraintes)
        self.ajouterCont.setStyleSheet("background-color: #035283; color: white;")
        self.ajouterCont.clicked.connect(self.addContraintes)
        self.addObj.clicked.connect(self.addObjCont)
        self.addObj.setStyleSheet("background-color: #035283; color: white;")
        self.hideElements()

    def hideElements(self):
        self.add.hide()
        self.table1.hide()
        self.label_4.hide()
        self.ajouterCont.hide()
        self.cont.hide()
        self.tableCont.hide()
        self.label_2.hide()
        self.label_7.hide()
        self.tableObj.hide()
        self.addObj.hide()
        self.label_8.hide()
        self.tableEl.hide()
        self.addEl.hide()
        self.opt.hide()
        self.resLabel.hide()
        self.result.hide()


    def numContraintes(self):
        num=self.numCont.toPlainText()
        if num:
            if num.isdigit():
                global numCont
                numCont=int(num)
                self.show0()
            else :
                self.show_error_message("Ajouter un nombre valide")
                return
        self.numCont.clear()
        
    def addContraintes(self):
        if numCont!=0 and numCont>len(contraintes):
            cont=self.cont.toPlainText()
            if cont:
                if cont.isalpha():
                    row_position = self.tableCont.rowCount()
                    self.tableCont.insertRow(row_position)
                    self.tableCont.setItem(row_position, 0, QtWidgets.QTableWidgetItem(cont))
                    delete_button = QtWidgets.QPushButton("Supp")
                    delete_button.clicked.connect(lambda _, row=row_position: self.deleteCont(row))
                    self.tableCont.setCellWidget(row_position, 1, delete_button)
                    contraintes.append(cont)
                else :
                    self.show_error_message("Ajouter une contrainte valide")
                    return
            
        if numCont==0:
            self.show_error_message("Ajouter le nombre de contraintes")
            return
        if len(contraintes)==numCont:
            self.show1()
            return
        self.cont.clear()
        
    def show0(self):
        self.label_4.show()
        self.cont.show()
        self.ajouterCont.show()
        self.tableCont.show()

    def show1(self):
        self.table1.setColumnCount(numCont+3)
        self.table1.setHorizontalHeaderLabels(["Element"]+contraintes+["Cout", "Delete"])
        self.table1.show()
        self.add.show()
        self.label_2.show()
        self.label_7.show()
        self.tableObj.show()
        self.addObj.show()
        self.label_8.show()
        self.tableEl.show()
        self.addEl.show()
        self.opt.show()
        self.resLabel.show()
        self.result.show()

    def deleteCont(self, row):
        self.tableCont.removeRow(row)
        contraintes.pop(row)
        self.tableCont.setRowCount(self.tableCont.rowCount()-1)



    def open_dialog(self):
        dialog = AddItemDialog()
        dialog.setWindowTitle("Ajouter un element")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            item, cont, cout = dialog.get_data()
            if item and cont and cout and len(cont)==numCont:
                row_position = self.table1.rowCount()
                self.table1.insertRow(row_position)
                self.table1.setItem(row_position, 0, QtWidgets.QTableWidgetItem(item))
                for i in range(numCont):
                    self.table1.setItem(row_position, i+1, QtWidgets.QTableWidgetItem(cont[i]))
                self.table1.setItem(row_position, numCont+1, QtWidgets.QTableWidgetItem(cout))
                delete_button = QtWidgets.QPushButton("Supp")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_row1(row))
                self.table1.setCellWidget(row_position, numCont+2, delete_button)
                elements.append([item]+cont+[cout])
                print(elements)
            

            else :
                self.show_error_message("Remplir tous les champs")
                return
            
    def delete_row1(self, row):
        #delete the the element from elementsCont
        for i in range(len(elementsCont)):
            if elementsCont[i][0] == elements[row][0]:
                elementsCont.pop(i)
                self.tableEl.removeRow(i)
                break
        self.table1.removeRow(row)
        elements.pop(row)

    def addElCont(self):
        dialog = AddElementContDialog('element')
        dialog.setWindowTitle("Ajouter une contrainte sur un element")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            constraint, valeur = dialog.get_data()

            if constraint and valeur:
                if not valeur.isdigit():
                    self.show_error_message("Ajouter une valeur valide")
                    return
                row_position = self.tableEl.rowCount()
                self.tableEl.insertRow(row_position)

                self.tableEl.setItem(row_position, 0, QtWidgets.QTableWidgetItem(constraint))
                self.tableEl.setItem(row_position, 1, QtWidgets.QTableWidgetItem(valeur))

                delete_button = QtWidgets.QPushButton("Supp")
                delete_button.clicked.connect(lambda _, row=row_position: self.deleteElCont(row,'element'))
                self.tableEl.setCellWidget(row_position, 2, delete_button)
                elementsCont.append([constraint, valeur])
                print(elementsCont)
            
            else :
                self.show_error_message("Veillez remplir tous les champs")
                return
            
    def addObjCont(self):
        dialog = AddElementContDialog('obj')
        dialog.setWindowTitle("Ajouter une contrainte sur un objectif")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            constraint, valeur = dialog.get_data()

            if constraint and valeur:
                if not valeur.isdigit():
                    self.show_error_message("Ajouter une valeur valide")
                    return
                row_position = self.tableObj.rowCount()
                self.tableObj.insertRow(row_position)

                self.tableObj.setItem(row_position, 0, QtWidgets.QTableWidgetItem(constraint))
                self.tableObj.setItem(row_position, 1, QtWidgets.QTableWidgetItem(valeur))

                delete_button = QtWidgets.QPushButton("Supp")
                delete_button.clicked.connect(lambda _, row=row_position: self.deleteElCont(row,'obj'))
                self.tableObj.setCellWidget(row_position, 2, delete_button)
                objectifs.append([constraint, valeur])
                print(objectifs)
            else :
                self.show_error_message("Veillez remplir tous les champs")
                return
            
    def deleteElCont(self, row,str):
        print(row)
        if str=='element':
            self.tableEl.removeRow(row)
            elementsCont.pop(row)
        else:
            self.tableObj.removeRow(row)
            objectifs.pop(row)
        
    

    def optimise(self):
        if items and constraints:
            if proteines and calories and calcium:
                nb_items = len(items)
                names = [item[0] for item in items]
                cout = [int(item[4]) for item in items]
                constraintsInf= []
                constraintsSup = []

                for i in range(len(constraints)):
                    temp = [0]*nb_items
                    for j in range(nb_items):
                        if constraints[i][0] == names[j]:
                            temp[j] = 1
                            break
                    temp.append(int(constraints[i][1]))
                    constraintsSup.append(temp)
                const = [proteines, calories, calcium]
                for i in range(3):
                    temp = []
                    for j in range(nb_items):
                        temp.append(items[j][i+1])
                    temp.append(int(const[i]))
                    constraintsInf.append(temp)
                # call the optimization function to get the result 
                x=optimize(nb_items, names, cout, constraintsInf, constraintsSup)
                if x:
                    self.result.show()
                    self.resLabel.hide()
                # Clear existing table content
                    self.result.clearContents()
                    # Set row and column count
                    self.result.setRowCount(len(items))

                    for i in range(nb_items):
                        self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(str(items[i][0])))
                        self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(str(x[i])))
                else :
                    self.resLabel.show()
                    self.resLabel.setText("Pas de solution trouvée")
                    self.resLabel.adjustSize()
                    self.result.hide()
            else:
                self.show_error_message("Ajouter les objectifs")

    def show_error_message(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

       



