# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'notice.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
    QSizePolicy, QToolButton, QWidget)

class Ui_notice(object):
    def setupUi(self, notice):
        if not notice.objectName():
            notice.setObjectName(u"notice")
        notice.resize(275, 60)
        notice.setMinimumSize(QSize(275, 60))
        notice.setMaximumSize(QSize(275, 60))
        self.centralwidget = QWidget(notice)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.btn = QToolButton(self.centralwidget)
        self.btn.setObjectName(u"btn")

        self.gridLayout.addWidget(self.btn, 0, 1, 2, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(True)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        notice.setCentralWidget(self.centralwidget)

        self.retranslateUi(notice)

        QMetaObject.connectSlotsByName(notice)
    # setupUi

    def retranslateUi(self, notice):
        notice.setWindowTitle(QCoreApplication.translate("notice", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("notice", u"\u795e\u9f99\u7c98\u8d34\u6b63\u5728\u8fd0\u884c", None))
        self.btn.setText(QCoreApplication.translate("notice", u"\u7acb\u5373\u505c\u6b62", None))
        self.label_2.setText(QCoreApplication.translate("notice", u"\u6309\u4e0bctrl+shift+alt+F1\u7acb\u5373\u505c\u6b62", None))
    # retranslateUi

