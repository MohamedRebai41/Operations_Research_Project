from PyQt5 import QtWidgets, uic

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
        lipides = self.text4.toPlainText()
        cout = self.text5_1.toPlainText()
        return item, proteine, calories, lipides, cout

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

class Window1(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window1, self).__init__()
        uic.loadUi('./window1.ui', self)
        self.button1.clicked.connect(self.open_dialog)
        self.button1.setStyleSheet("background-color: #8c4669; color: white;")
        self.table1.setColumnCount(6)  
        self.table2.setColumnCount(3)
        self.add.clicked.connect(self.add_constraint)
        self.add.setStyleSheet("background-color: #8c4669; color: white;")
        self.opt.setStyleSheet("background-color: #8c4669; color: white;")
        self.opt.clicked.connect(self.optimise)
        self.add1.setStyleSheet("background-color: #8c4669; color: white;")
        self.add1.clicked.connect(self.getBasicConstraints)
        
    def getBasicConstraints(self):
        proteines=self.cont1.toPlainText()
        calories=self.cont2.toPlainText()
        lipides=self.cont3.toPlainText()

        if proteines and calories and lipides:
            constraints.append(["proteines", proteines])
            constraints.append(["calories", calories])
            constraints.append(["lipides", lipides])
            #add the constraints to the table
            for i in range(3):
                row_position = self.table2.rowCount()
                self.table2.insertRow(row_position)
                self.table2.setItem(row_position, 0, QtWidgets.QTableWidgetItem(constraints[i][0]))
                self.table2.setItem(row_position, 1, QtWidgets.QTableWidgetItem(constraints[i][1]))
                delete_button = QtWidgets.QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_row2(row))
                self.table2.setCellWidget(row_position, 2, delete_button)
    

    def open_dialog(self):
        dialog = AddItemDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            item, proteine, calories, lipides, cout = dialog.get_data()

            if item and proteine and calories and lipides and cout:
                row_position = self.table1.rowCount()
                self.table1.insertRow(row_position)

                self.table1.setItem(row_position, 0, QtWidgets.QTableWidgetItem(item))
                self.table1.setItem(row_position, 1, QtWidgets.QTableWidgetItem(proteine))
                self.table1.setItem(row_position, 2, QtWidgets.QTableWidgetItem(calories))
                self.table1.setItem(row_position, 3, QtWidgets.QTableWidgetItem(lipides))
                self.table1.setItem(row_position, 4, QtWidgets.QTableWidgetItem(cout))

                delete_button = QtWidgets.QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_row1(row))
                self.table1.setCellWidget(row_position, 5, delete_button)  
                items.append([item, proteine, calories, lipides, cout])
                print(items)

    def add_constraint(self):
        dialog = AddConstraintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            constraint, valeur = dialog.get_data()

            if constraint and valeur:
                row_position = self.table2.rowCount()
                self.table2.insertRow(row_position)

                self.table2.setItem(row_position, 0, QtWidgets.QTableWidgetItem(constraint))
                self.table2.setItem(row_position, 1, QtWidgets.QTableWidgetItem(valeur))

                delete_button = QtWidgets.QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.delete_row2(row))
                self.table2.setCellWidget(row_position, 2, delete_button)
                constraints.append([constraint, valeur])
                print(constraints)

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
        proteines=self.cont1.toPlainText()
        calories=self.cont2.toPlainText()
        lipides=self.cont3.toPlainText()
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
        const = [proteines, calories, lipides]
        for i in range(3):
            temp = []
            for j in range(nb_items):
                temp.append(items[j][i+1])
            temp.append(int(const[i]))
            constraintsInf.append(temp)
        # call the optimization function to get the result 
        x=optimize(nb_items, names, cout, constraintsInf, constraintsSup)

#bech taccedi lel partie eli bech tekteb feha self.result

