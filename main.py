import sys
from window import *
from model import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow(self)
        self.ui.setupUi(self)

        img1 = cv.imread('nature.jpg')
        assert img1 is not None
        
        self.model = FilterDleGame(1, 5, 1, [img1])
        filtered_img = self.model.get_filteredImage()
        
        assert filtered_img is not None
        assert len(filtered_img.shape) == 3

        print(self.model._correct_filters)
        print(self.model.guess_filterclass(ColorFilter))

        self.show()

        self.ui.change_image(filtered_img)


    def make_guess(self, filter_list: list[FilterObject]):
        for f_obj in filter_list:
            print(f_obj.filter_categ)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wd = MainWindow()
    wd.show()
    sys.exit(app.exec())