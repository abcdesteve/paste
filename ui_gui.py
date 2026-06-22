# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QPlainTextEdit, QSizePolicy, QWidget)

class Ui_gui(object):
    def setupUi(self, gui):
        if not gui.objectName():
            gui.setObjectName(u"gui")
        gui.resize(300, 100)
        self.centralwidget = QWidget(gui)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setFrameShape(QFrame.NoFrame)
        self.plainTextEdit.setUndoRedoEnabled(False)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.horizontalLayout.addWidget(self.plainTextEdit)

        gui.setCentralWidget(self.centralwidget)

        self.retranslateUi(gui)

        QMetaObject.connectSlotsByName(gui)
    # setupUi

    def retranslateUi(self, gui):
        gui.setWindowTitle(QCoreApplication.translate("gui", u"\u795e\u9f99\u7c98\u8d34", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("gui", u"\u6b63\u5728\u7c98\u8d34\u4ee5\u4e0b\u5185\u5bb9", None))
    # retranslateUi

