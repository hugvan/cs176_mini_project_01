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
        
        self.model = FilterDleGame(1, 5, 2, [img1])
        filtered_img = self.model.get_filteredImage()
        
        assert filtered_img is not None
        assert len(filtered_img.shape) == 3

        self.show()

        self.ui.change_image(filtered_img)


    def make_guess(self, filter_list: list[FilterObject]):
        
        g_obj = []
        for f_obj in filter_list:
            categ = f_obj.filter_categ
            option: Enum = categ[f_obj.drop.currentText()] # type: ignore
            option_obj = option.value()

            verd = self.model.check_combined(categ, option_obj)
            
            g_portion: GPortion = verd, categ, option
            g_obj.append(g_portion)
        
        self.ui.add_guess_object(tuple(g_obj))

    def next_round(self, image_path: str):
        
        img1 = cv.imread(image_path)
        assert img1 is not None
        
        self.model = FilterDleGame(1, 5, 2, [img1])
        filtered_img = self.model.get_filteredImage()
        
        assert filtered_img is not None
        assert len(filtered_img.shape) == 3

        self.ui.change_image(filtered_img)
        self.ui.remove_guess_objects()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    wd = MainWindow()
    wd.show()
    sys.exit(app.exec())