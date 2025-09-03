import sys
from window import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wd = MainWindow()
    wd.show()
    sys.exit(app.exec())