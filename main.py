import sys
import keyboard
import pyperclip
import qdarkstyle
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# from pynput.keyboard import Controller


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(self.windowFlags() | Qt.WindowFullScreen | Qt.WindowOverridesSystemGestures | Qt.WindowStaysOnTopHint)
        # self.setWindowOpacity(0.01)


class Tray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.setup()
        self.setIcon(QIcon('icon.png'))
        self.show()
        QMessageBox.information(win, '神龙粘贴v1.0', '神龙粘贴已启动\n\n请查看系统托盘')

    def setup(self):
        self.menu = QMenu()
        # self.win = Main()
        self.type_mode = '逐字'
        self.index = 0

        # self.keyboard = Controller()

        keyboard.add_hotkey('ctrl+shift+alt+space', self.paste)
        self.action_paste = QAction('粘贴', self, triggered=self.delay_paste)
        self.menu.addAction(self.action_paste)
        self.action_mode = QAction('切换模式:{}'.format(
            self.type_mode), self, triggered=self.change_mode)
        self.menu.addAction(self.action_mode)
        self.history = QMenu('历史')
        self.menu.addMenu(self.history)
        self.menu.addAction(QAction('退出', self, triggered=sys.exit))
        self.setContextMenu(self.menu)

        self.timer = QTimer()
        self.timer.start(250)
        self.timer.timeout.connect(self.update)

    def change_mode(self):
        if self.type_mode == '连续':
            self.type_mode = '逐字'
        else:
            self.type_mode = '连续'
        self.action_mode.setText('切换模式:{}'.format(self.type_mode))

    def update(self):
        txt = pyperclip.paste()
        if txt:
            self.setToolTip(
                '当前模式:{}\n当前剪贴板内容:\n{}'.format(self.type_mode, txt))
            action = QAction(
                txt, self, triggered=lambda: self.delay_paste(txt))
            if len(self.history.actions()) == 0:
                self.history.addAction(action)
            elif hash(txt) != hash(self.history.actions()[-1].text()):
                self.history.addAction(action)
            if len(self.history.actions()) == 11:
                self.history.removeAction(self.history.actions()[0])

    # def history_paste(self):
    #     # print(self.history.activeAction().text())
    #     print([i for i in self.history.actions() if i.isChecked()][0])
        # temp=self.history.activeAction()
        # time.sleep(5)
        # self.paste()

    def delay_paste(self, txt=''):
        QTimer.singleShot(5000, lambda: self.paste(txt))

    def paste(self, txt=''):
        if txt == '':
            txt = pyperclip.paste()
        print('paste:', txt)
        if self.type_mode == '连续':
            # self.keyboard.type(txt)
            keyboard.write(txt)
        else:
            # for i in txt:
            #     time.sleep(0.001)
            # self.keyboard.type(i)
            keyboard.write(txt, 0.1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))
    win = Main()
    tray = Tray()
    sys.exit(app.exec())
