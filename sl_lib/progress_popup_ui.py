# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress_popup.ui'
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
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (ImageLabel, IndeterminateProgressBar, ProgressBar)

class Ui_progress_popup(object):
    def setupUi(self, progress_popup):
        if not progress_popup.objectName():
            progress_popup.setObjectName(u"progress_popup")
        progress_popup.resize(400, 250)
        progress_popup.setMinimumSize(QSize(400, 250))
        progress_popup.setMaximumSize(QSize(400, 250))
        self.verticalLayout_4 = QVBoxLayout(progress_popup)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_upper = QFrame(progress_popup)
        self.frame_upper.setObjectName(u"frame_upper")
        self.frame_upper.setFrameShape(QFrame.NoFrame)
        self.frame_upper.setFrameShadow(QFrame.Plain)
        self.frame_upper.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.frame_upper)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_title = QLabel(self.frame_upper)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(16)
        self.label_title.setFont(font)
        self.label_title.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_title)

        self.label_current = QLabel(self.frame_upper)
        self.label_current.setObjectName(u"label_current")
        font1 = QFont()
        font1.setPointSize(10)
        self.label_current.setFont(font1)
        self.label_current.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_current)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.ImageLabel = ImageLabel(self.frame_upper)
        self.ImageLabel.setObjectName(u"ImageLabel")
        self.ImageLabel.setMinimumSize(QSize(75, 75))
        self.ImageLabel.setMaximumSize(QSize(75, 75))

        self.horizontalLayout.addWidget(self.ImageLabel)


        self.verticalLayout_4.addWidget(self.frame_upper)

        self.frame_lower = QFrame(progress_popup)
        self.frame_lower.setObjectName(u"frame_lower")
        self.frame_lower.setStyleSheet(u"QFrame{border-radius: 10px;}")
        self.frame_lower.setFrameShape(QFrame.NoFrame)
        self.frame_lower.setFrameShadow(QFrame.Plain)
        self.frame_lower.setLineWidth(0)
        self.verticalLayout_3 = QVBoxLayout(self.frame_lower)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_progress = QLabel(self.frame_lower)
        self.label_progress.setObjectName(u"label_progress")

        self.horizontalLayout_2.addWidget(self.label_progress)

        self.label_progress_data = QLabel(self.frame_lower)
        self.label_progress_data.setObjectName(u"label_progress_data")

        self.horizontalLayout_2.addWidget(self.label_progress_data)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_time_past = QLabel(self.frame_lower)
        self.label_time_past.setObjectName(u"label_time_past")

        self.horizontalLayout_3.addWidget(self.label_time_past)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.label_time_left = QLabel(self.frame_lower)
        self.label_time_left.setObjectName(u"label_time_left")

        self.horizontalLayout_3.addWidget(self.label_time_left)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 6, -1, -1)
        self.ProgressBar = ProgressBar(self.frame_lower)
        self.ProgressBar.setObjectName(u"ProgressBar")

        self.verticalLayout_2.addWidget(self.ProgressBar)

        self.IndeterminateProgressBar = IndeterminateProgressBar(self.frame_lower)
        self.IndeterminateProgressBar.setObjectName(u"IndeterminateProgressBar")

        self.verticalLayout_2.addWidget(self.IndeterminateProgressBar)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addWidget(self.frame_lower)


        self.retranslateUi(progress_popup)

        QMetaObject.connectSlotsByName(progress_popup)
    # setupUi

    def retranslateUi(self, progress_popup):
        progress_popup.setWindowTitle(QCoreApplication.translate("progress_popup", u"Form", None))
#if QT_CONFIG(accessibility)
        self.frame_lower.setAccessibleDescription(QCoreApplication.translate("progress_popup", u"dialog_lower_frame", None))
#endif // QT_CONFIG(accessibility)
        self.label_progress.setText(QCoreApplication.translate("progress_popup", u"\u5f53\u524d\u8fdb\u5ea6\uff1a", None))
        self.label_progress_data.setText("")
        self.label_time_past.setText(QCoreApplication.translate("progress_popup", u"\u5df2\u7528\u65f6\u95f4\uff1a0s", None))
        self.label_time_left.setText(QCoreApplication.translate("progress_popup", u"\u5269\u4f59\u65f6\u95f4\uff1a\u6b63\u5728\u8ba1\u7b97", None))
    # retranslateUi

