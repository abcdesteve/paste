# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'input_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

from qfluentwidgets import (EditableComboBox, LineEdit, PrimaryPushButton, PushButton)

class Ui_input_dialog(object):
    def setupUi(self, input_dialog):
        if not input_dialog.objectName():
            input_dialog.setObjectName(u"input_dialog")
        input_dialog.resize(350, 250)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(input_dialog.sizePolicy().hasHeightForWidth())
        input_dialog.setSizePolicy(sizePolicy)
        input_dialog.setMinimumSize(QSize(300, 200))
        self.verticalLayout = QVBoxLayout(input_dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_upper = QFrame(input_dialog)
        self.frame_upper.setObjectName(u"frame_upper")
        self.frame_upper.setFrameShape(QFrame.NoFrame)
        self.frame_upper.setFrameShadow(QFrame.Plain)
        self.frame_upper.setLineWidth(0)
        self.verticalLayout_3 = QVBoxLayout(self.frame_upper)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.title = QLabel(self.frame_upper)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(16)
        self.title.setFont(font)

        self.verticalLayout_3.addWidget(self.title)

        self.content = QLabel(self.frame_upper)
        self.content.setObjectName(u"content")
        font1 = QFont()
        font1.setPointSize(11)
        self.content.setFont(font1)
        self.content.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.content)


        self.verticalLayout.addWidget(self.frame_upper)

        self.frame_lower = QFrame(input_dialog)
        self.frame_lower.setObjectName(u"frame_lower")
        self.frame_lower.setStyleSheet(u"QFrame{border-radius: 10px;}")
        self.frame_lower.setFrameShape(QFrame.NoFrame)
        self.frame_lower.setFrameShadow(QFrame.Plain)
        self.frame_lower.setLineWidth(0)
        self.verticalLayout_2 = QVBoxLayout(self.frame_lower)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.comboBox = EditableComboBox(self.frame_lower)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_2.addWidget(self.comboBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_cancel = PushButton(self.frame_lower)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_2.addWidget(self.btn_cancel)

        self.btn_ok = PrimaryPushButton(self.frame_lower)
        self.btn_ok.setObjectName(u"btn_ok")
        self.btn_ok.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_2.addWidget(self.btn_ok)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.frame_lower)


        self.retranslateUi(input_dialog)

        QMetaObject.connectSlotsByName(input_dialog)
    # setupUi

    def retranslateUi(self, input_dialog):
        input_dialog.setWindowTitle(QCoreApplication.translate("input_dialog", u"Form", None))
#if QT_CONFIG(accessibility)
        self.frame_lower.setAccessibleDescription(QCoreApplication.translate("input_dialog", u"dialog_lower_frame", None))
#endif // QT_CONFIG(accessibility)
        self.btn_cancel.setText(QCoreApplication.translate("input_dialog", u"\u53d6\u6d88", None))
        self.btn_ok.setText(QCoreApplication.translate("input_dialog", u"\u786e\u5b9a", None))
    # retranslateUi

