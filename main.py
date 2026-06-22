import sys
import os
import time
import keyboard
import pyperclip
import qdarkstyle
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from ui_gui import Ui_notice

# from pynput.keyboard import Controller


class Main(QMainWindow, Ui_notice):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint | Qt.CoverWindow)

        self.stop_flag = False

        self.animation = QPropertyAnimation(self, b'pos')
        self.animation.setDuration(500)

        self.btn.clicked.connect(self.stop)

        QTimer.singleShot(0, self.hide_animation)
        # QTimer.singleShot(1000, self.show)
        # self.setWindowOpacity(0.75)
        self.show()

    def stop(self):
        self.stop_flag = True

    @Slot()
    def show_animation(self):
        self.animation.setEasingCurve(QEasingCurve.OutBack)
        pos_x = QGuiApplication.primaryScreen().size().width()//2-self.width()//2
        self.animation.setStartValue(QPoint(pos_x, -self.height()))
        self.animation.setEndValue(QPoint(pos_x, 0))
        self.animation.start()

    @Slot()
    def hide_animation(self):
        self.animation.setEasingCurve(QEasingCurve.InBack)
        pos_x = QGuiApplication.primaryScreen().size().width()//2-self.width()//2
        self.animation.setStartValue(QPoint(pos_x, 0))
        self.animation.setEndValue(QPoint(pos_x, -self.height()))
        self.animation.start()


class Tray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.setup()
        self.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), 'icon.png')))
        self.show()

    def setup(self):
        self.menu = QMenu()
        # self.win = Main()
        self.type_mode = '逐字'
        self.index = 0

        # self.keyboard = Controller()

        keyboard.add_hotkey('ctrl+shift+alt+space',
                            self.paste, suppress=True,timeout=3,trigger_on_release=True)
        self.action_paste = QAction('粘贴', self, triggered=self.delay_paste)
        self.action_mode = QAction(
            f'切换模式:{self.type_mode}', self, triggered=self.change_mode)
        self.action_history = QMenu('历史')
        self.action_setting = QAction('设置')

        self.menu.addActions([self.action_paste, self.action_mode])
        self.menu.addMenu(self.action_history)
        self.menu.addActions(
            [self.action_setting, QAction('退出', self, triggered=sys.exit)])
        self.setContextMenu(self.menu)

        self.timer = QTimer()
        self.timer.start(250)
        self.timer.timeout.connect(self.update_history)

    def change_mode(self):
        if self.type_mode == '连续':
            self.type_mode = '逐字'
        else:
            self.type_mode = '连续'
        self.action_mode.setText('切换模式:{}'.format(self.type_mode))

    def update_history(self):
        txt = pyperclip.paste()
        if txt:
            self.setToolTip(
                '当前模式:{}\n当前剪贴板内容:\n{}'.format(self.type_mode, txt))
            action = QAction(
                txt, self, triggered=lambda: self.delay_paste(txt))
            if len(self.action_history.actions()) == 0:
                self.action_history.addAction(action)
            elif hash(txt) != hash(self.action_history.actions()[-1].text()):
                self.action_history.addAction(action)
            if len(self.action_history.actions()) == 11:
                self.action_history.removeAction(
                    self.action_history.actions()[0])

    # def history_paste(self):
    #     # print(self.history.activeAction().text())
    #     print([i for i in self.history.actions() if i.isChecked()][0])
        # temp=self.history.activeAction()
        # time.sleep(5)
        # self.paste()

    def delay_paste(self, txt=''):
        QTimer.singleShot(5000, lambda: self.paste(txt))

    def paste(self, txt=''):
        QMetaObject.invokeMethod(win, "show_animation", Qt.QueuedConnection)
        # win.show_animation()

        if txt == '':
            txt = pyperclip.paste()
        print('paste:', txt)
        # if self.type_mode == '连续':
        #     # self.keyboard.type(txt)
        #     keyboard.write(txt)
        # else:
        #     # for i in txt:
        #     #     time.sleep(0.001)
        #     # self.keyboard.type(i)
        #     keyboard.write(txt, 0.01)
        
        time.sleep(0.5)
        for char in txt:
            if not win.stop_flag:
                keyboard.write(char)
                if self.type_mode == '连续':
                    time.sleep(0.001)
                elif self.type_mode == '逐字':
                    time.sleep(0.01)
            else:
                self.stop_flag = False
                break

        keyboard.release('ctrl+alt+shift')

        QMetaObject.invokeMethod(win, "hide_animation", Qt.QueuedConnection)
        # win.hide_animation()

    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icon.png')))
    win = Main()
    tray = Tray()
    QMessageBox.information(win, '神龙粘贴v1.2', '神龙粘贴已启动\n\n请查看系统托盘')
    sys.exit(app.exec())
