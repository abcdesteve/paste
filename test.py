from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ui_gui import Ui_notice
import sys
import qdarkstyle


class Notice(QMainWindow, Ui_notice):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint | Qt.CoverWindow)
        self.animation=QPropertyAnimation(self,b'pos')
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.OutBack)
        self.animation.setStartValue(QPoint(850,-50))
        self.animation.setEndValue(QPoint(850,0))
        self.animation.start()
        # self.setGeometry(QRect(QPoint(850, 0), self.size()))
        
        self.btn.clicked.connect(self.stop)
        # self.setWindowOpacity(0.75)
        self.show()

    def stop(self):
        self.animation.setEasingCurve(QEasingCurve.InBack)
        self.animation.setStartValue(QPoint(850,0))
        self.animation.setEndValue(QPoint(850,-50))
        self.animation.start()
        QTimer.singleShot(1000,app.exit)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))
    win = Notice()
    sys.exit(app.exec())
