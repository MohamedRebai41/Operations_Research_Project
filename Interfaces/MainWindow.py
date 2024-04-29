import sys
from PyQt5 import QtWidgets, uic
from window1 import Window1

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('./form.ui', self)
        self.button1.clicked.connect(self.on_button1_click)

    def on_button1_click(self):
        self.window1 = Window1()
        self.window1.show()

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
