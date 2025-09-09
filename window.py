from __future__ import annotations
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mini01_viewFGIHei.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from itertools import product

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon, QFileOpenEvent,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QMainWindow, QFileDialog,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem, QLayout,
    QStatusBar, QVBoxLayout, QWidget)
from PySide6.QtCore import Slot

from model import *

F_CATEGORY_STR: dict[type, str] = {
    ColorFilter: "Color",
    ContrastFilter: "Contrast", 
    BrightnessFilter: "Brightness", 
    ThresholdFilter: "Threshold", 
    EdgeFilter: "Edges", 
    BlurFilter: "Blur",
    TranslateFilter: "Translate",
    RotateFilter: "Rotate",
    SkewFilter: "Skew"
} 



class GuessButton(QPushButton):
    def __init__(self, controller, parent=None):
        QPushButton.__init__(self)

        self.filters_checked = []
        self.controller = controller
        self.update_viability()
        self.clicked.connect(self.press_button)

        self.setObjectName(u"make_guess_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy2)
        self.setMinimumSize(QSize(100, 50))
        self.setText(QCoreApplication.translate("MainWindow", "Make Guess", None))
    
    def check_callback(self, is_add: bool, filt: FilterObject):
        if (is_add):
            self.filters_checked.append(filt)
        else:
            self.filters_checked.remove(filt)
        
        self.update_viability()

    def update_viability(self):
        exact_clicks = len(self.filters_checked) == 2
        self.setEnabled(exact_clicks)
        self.setStyleSheet(";" if exact_clicks else "color: gray;") 

    @Slot()
    def press_button(self):
        self.controller.make_guess(self.filters_checked)

class NextRoundButton(QPushButton):
    def __init__(self, controller, parent=None):
        QPushButton.__init__(self)

        self.controller = controller
        self.clicked.connect(self.press_button)
        
        self.setObjectName(u"next_round_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy2)
        self.setMinimumSize(QSize(100, 50))
        self.setText(QCoreApplication.translate("MainWindow", "New Round", None))
    
    
    @Slot()
    def press_button(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None,  # Parent widget (None for no parent)
            "Open File",  # Dialog title
            "",  # Initial directory (empty string for current directory)
            "Images (*.jpg *.png *.bmp);;All Files (*)"  # File filters
        )

        self.controller.next_round(file_path)


class FilterObject(QFrame):
    def __init__(self, filter_categ: type, guess_btn: GuessButton, parent=None):
        self.filter_categ = filter_categ
        self.filter_options = [m.name for m in filter_categ]  # type: ignore
        self.guess_btn = guess_btn
        
        QFrame.__init__(self)
        
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        
        self.setObjectName("filter_object")
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet("background-color: none;") 
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setLineWidth(5)
        self.setMidLineWidth(1)
        
        vlayout = QVBoxLayout(self)
        vlayout.setObjectName("vlayout")
        self.check = QCheckBox(self)
        self.check.setObjectName("filter_check")
        filter_name = F_CATEGORY_STR[filter_categ]
        self.check.setText( QCoreApplication.translate("MainWindow", filter_name, None) )
        sizePolicy1.setHeightForWidth(self.check.sizePolicy().hasHeightForWidth())
        self.check.setSizePolicy(sizePolicy1)

        self.check.clicked.connect(self.press_button)

        vlayout.addWidget(self.check)

        
        self.drop = QComboBox(self)
        for option in self.filter_options:
            self.drop.addItem(option)

        self.drop.setObjectName("filter_drop")
        self.drop.setStyleSheet("color: rgb(0, 0, 0);")
        sizePolicy1.setHeightForWidth(self.drop.sizePolicy().hasHeightForWidth())
        self.drop.setSizePolicy(sizePolicy1)

        vlayout.addWidget(self.drop)
    
    @Slot()
    def press_button(self):
        is_checked = self.check.isChecked()
        
        self.guess_btn.check_callback(is_checked, self)
        
        if is_checked:
            self.check.setStyleSheet("color: green;") 
        else:
            self.check.setStyleSheet(";") 


GPortion = tuple[Verdict, type, Enum]
GObject = tuple[GPortion, GPortion]

class GuessObject(QHBoxLayout):
    def __init__(self, guess: GObject, s_parent):
        
        QHBoxLayout.__init__(self)
        
        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        
        self.setObjectName("guess_object")
        
        def add_guess_portion(verdict: Verdict, f_name: type, f_option: Enum):
            guess_portion = QFrame(s_parent)
            guess_portion.setObjectName("guess_portion")
            size_policy.setHeightForWidth(guess_portion.sizePolicy().hasHeightForWidth())
            guess_portion.setSizePolicy(size_policy)
            
            if verdict == Verdict.IncorrectClassGuess:
                bg_color = "rgb(127, 127, 127)"
            elif verdict == Verdict.IncorrectFilterGuess:
                bg_color = "rgb(255, 255, 127)"
            else:
                bg_color = "rgb(127, 255, 127)"
            
            guess_portion.setStyleSheet(f"background-color: {bg_color};\n"
            "color: rgb(0, 0, 0);")
            guess_portion.setFrameShape(QFrame.Shape.StyledPanel)
            guess_portion.setFrameShadow(QFrame.Shadow.Sunken)
            
            vlayout = QVBoxLayout(guess_portion)
            vlayout.setSpacing(0)
            vlayout.setObjectName("vlayout")
            
            guess_filter_name = QLabel(guess_portion)
            guess_filter_name.setObjectName("guess_filter_name")
            guess_filter_name.setTextFormat(Qt.TextFormat.RichText)
            guess_filter_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            f_name_str = F_CATEGORY_STR[f_name]
            guess_filter_name.setText(QCoreApplication.translate("MainWindow", f_name_str, None))

            vlayout.addWidget(guess_filter_name)

            guess_option = QLabel(guess_portion)
            guess_option.setObjectName("guess_option")
            guess_option.setTextFormat(Qt.TextFormat.RichText)
            guess_option.setAlignment(Qt.AlignmentFlag.AlignCenter)
            guess_option.setText(QCoreApplication.translate("MainWindow", 
                f"<html><head/><body><p><span style=\" font-weight:700;\">{f_option.name}</span></p></body></html>", None))

            vlayout.addWidget(guess_option)

            self.addWidget(guess_portion)


        gp1, gp2 = guess
        add_guess_portion(gp1[0], gp1[1], gp1[2])
        add_guess_portion(gp2[0], gp2[1], gp2[2])

class Ui_MainWindow(object):

    def __init__(self, controller) -> None:
        self.controller = controller

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(671, 563)
        MainWindow.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        MainWindow.setStyleSheet(u"background-color: rgb(36, 53, 74);\n""color: rgb(255, 255, 255);")
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        
        self.vlayout_left = QVBoxLayout()
        self.vlayout_left.setObjectName(u"vlayout_left")
        
        self.title_label = QLabel(self.centralwidget)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMaximumSize(QSize(16777215, 51))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vlayout_left.addWidget(self.title_label)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

        self.make_guess_button = GuessButton(self.controller, self.centralwidget)

        for i, j in product(range(3), range(3)):
            f_type = filter_classes[i*3 + j]
            f_obj = FilterObject(f_type, self.make_guess_button, parent=self.vlayout_left)
            self.gridLayout.addWidget(f_obj, i, j, 1, 1)
        
        self.vlayout_left.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.horizontalLayout.addWidget(self.make_guess_button)
        
        self.new_round_button = NextRoundButton(self.controller, self.centralwidget)
        self.horizontalLayout.addWidget(self.make_guess_button)
        self.horizontalLayout.addItem(self.horizontalSpacer_2)
        
        self.vlayout_left.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vlayout_left.addWidget(self.new_round_button)
        self.vlayout_left.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.vlayout_left)

        self.vlayout_right = QVBoxLayout()
        self.vlayout_right.setObjectName(u"vlayout_right")
        self.guessed_image = QLabel(self.centralwidget)
        self.guessed_image.setObjectName(u"guessed_image")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.guessed_image.sizePolicy().hasHeightForWidth())
        self.guessed_image.setSizePolicy(sizePolicy3)
        self.guessed_image.setMaximumSize(QSize(444, 250))
        
        self.guessed_image.setScaledContents(True)
        self.guessed_image.setStyleSheet(u"background-color: rgb(0, 0, 0);")

        self.vlayout_right.addWidget(self.guessed_image)

        self.guess_container = QFrame(self.centralwidget)
        self.guess_container.setObjectName(u"guess_container")
        self.guess_container.setStyleSheet(u"background-color: rgb(28, 41, 57);")
        self.guess_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.guess_container.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout_17 = QVBoxLayout(self.guess_container)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        

        self.verticalSpacer = QSpacerItem(20, 198, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer)


        self.vlayout_right.addWidget(self.guess_container)


        self.horizontalLayout_2.addLayout(self.vlayout_right)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 671, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def change_image(self, image_mat):
        s = image_mat.shape
        width, height = s[1], s[0]
        ratio = width / height
        q_image = QImage(image_mat, width, height, QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)
        self.guessed_image.setPixmap(pixmap)
        self.guessed_image.setMaximumSize(QSize(200 * ratio, 200))

    def add_guess_object(self, guess: GObject):
        g_obj =  GuessObject(guess, self.guess_container)
        num_elem =  len(self.verticalLayout_17.children())
        self.verticalLayout_17.insertLayout(num_elem, g_obj)

    def remove_guess_objects(self):
        pLayout = self.verticalLayout_17
                
        for i in reversed(range(pLayout.count())): 
            y = pLayout.itemAt(i)
            if not isinstance(y, GuessObject): continue
            
            clear_layout(y)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.guessed_image.setText("")
        self.title_label.setText(QCoreApplication.translate("MainWindow", "<html><head/><body><p><span style=\" font-size:28pt; font-weight:700;\">FILTERDLE</span></p></body></html>", None))
        
        

def clear_layout(layout: QLayout):
    """
    Recursively clears a QLayout and its contents (widgets and sub-layouts).
    """
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()  # Delete the widget
        elif item.layout():
            clear_layout(item.layout())  # Recursively clear sub-layouts
        # The QLayoutItem itself will be deleted when its parent layout is deleted