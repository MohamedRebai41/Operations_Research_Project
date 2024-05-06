import sys
from PyQt5 import QtWidgets, uic

class AddItemDialog(QtWidgets.QDialog):
    def __init__(self):
        super(AddItemDialog, self).__init__()
        uic.loadUi('./itemForm.ui', self)  
        # self.button.clicked.connect(self.accept)
        # self.button.setStyleSheet("background-color: #8c4669; color: white;")
        self.create_input_fields(5)

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
            input_field.setObjectName(f"Contraintes_{i}")
            input_field.setPlaceholderText(f"Contrainte {i}")
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
        self.button.setStyleSheet("background-color: #8c4669; color: white;")
        self.button.clicked.connect(self.accept)

        #adjust window size
        self.setFixedSize(200 + (numCont+2)*110, 100)

    

    def get_data(self):
        element = self.element_input.text()
        cont = [input_field.toPlainText() for input_field in self.cont_inputs]
        cout = self.cout_input.text()
        return element, cont, cout


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AddItemDialog()
    window.show()
    sys.exit(app.exec_())
