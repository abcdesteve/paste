from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qfluentwidgets import *

import theme_control

import sys
import time
import keyboard
import threading

APP_NAME = '神龙粘贴'
APP_VERSION = '2.0'


class SystemTray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon('icon.png'))
        self.init_actions()
        self.setupUI()
        self.clipboard = app.clipboard()
        self.clipboard.dataChanged.connect(self.update)
        self.update()
        self.show()
        # self.timer=QTimer()
        # self.timer.setInterval(500)
        # self.timer.timeout.connect(self.update)
        # self.timer.start()

    def setupUI(self):
        self.menu = SystemTrayMenu(APP_NAME+' v'+APP_VERSION)
        self.menu.addAction(self.ac_paste)

        self.menu_history = RoundMenu('历史剪贴板')
        self.menu_history.addAction(self.ac_empty)
        self.menu_history.setIcon(FluentIcon.icon(FluentIcon.HISTORY))
        self.menu.addMenu(self.menu_history)

        self.menu_mode = CheckableMenu('粘贴模式', None, MenuIndicatorType.RADIO)
        self.menu_mode.addActions([self.ac_mode_wbw, self.ac_mode_aao])
        self.menu_mode.setIcon(FluentIcon.icon(FluentIcon.EDIT))
        self.menu.addMenu(self.menu_mode)
        # self.menu.add

        self.menu.addAction(self.ac_exit)
        self.setContextMenu(self.menu)

    def init_actions(self):
        self.ac_empty = QAction('(暂无记录)')
        self.ac_empty.setDisabled(True)
        self.ac_paste = QAction(FluentIcon.icon(
            FluentIcon.PASTE), '5s后粘贴', self, triggered=self.paste)
        self.ac_mode_wbw = QAction('逐字模式', self, checkable=True, checked=True,
                                   triggered=lambda: self.menu_mode.setActiveAction(self.menu_mode.actions()[0]))
        self.ac_mode_aao = QAction('整段模式', self, checkable=True, triggered=lambda: self.menu_mode.setActiveAction(
            self.menu_mode.actions()[1]))
        self.acgp_mode = QActionGroup(self)
        self.acgp_mode.addAction(self.ac_mode_wbw)
        self.acgp_mode.addAction(self.ac_mode_aao)
        self.ac_exit = QAction(FluentIcon.icon(
            FluentIcon.CLOSE), '退出', self, triggered=app.exit)

    def update(self):
        self.setToolTip(
            f"{APP_NAME} v{APP_VERSION}\n当前模式：{'逐字模式'if self.ac_mode_wbw.isChecked() else '整段模式'}\n{self.clipboard.text().strip()}")
        if self.clipboard.text().strip():
            self.menu_history.removeAction(self.ac_empty)
            self.menu_history.addAction(QAction(self.clipboard.text(
            ), self, triggered=lambda txt=self.clipboard.text(): self.paste(txt)))
            if len(self.menu_history.actions()) > 10:
                self.menu_history.removeAction(self.menu_history.actions()[0])

    def paste(self, txt='', delay=5000):
        def worker(txt):
            if txt:
                delay = 50 if self.ac_mode_wbw.isChecked() else 0
                for i in txt:
                    keyboard.write(i)
                    time.sleep(delay/1000)
                    if keyboard.is_pressed('ctrl'):
                        break
        if not txt:
            txt = self.clipboard.text()
        self.thread_paste = threading.Thread(target=worker, args=(txt,))
        QTimer.singleShot(delay, self.thread_paste.start)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    theme_control.apply_theme(app, 'auto')
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setWindowIcon(QIcon('icon.png'))
    tray = SystemTray()
    sys.exit(app.exec())
