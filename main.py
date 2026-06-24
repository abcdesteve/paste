from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qfluentwidgets import *

import theme_control

import re
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
        self.menu = SystemTrayMenu(APP_NAME + ' v' + APP_VERSION)
        self.menu.addAction(self.ac_paste)

        self.menu_history = RoundMenu('历史剪贴板')
        self.menu_history.addAction(self.ac_empty)
        self.menu_history.setIcon(FluentIcon.icon(FluentIcon.HISTORY))
        self.menu.addMenu(self.menu_history)

        # 设置
        self.menu_settings = RoundMenu('设置')
        self.menu_settings.setIcon(FluentIcon.icon(FluentIcon.SETTING))
        self.menu.addMenu(self.menu_settings)

        self.menu_mode = CheckableMenu('粘贴模式', None, MenuIndicatorType.RADIO)
        self.menu_mode.addActions([self.ac_mode_wbw, self.ac_mode_aao])
        self.menu_mode.setIcon(FluentIcon.icon(FluentIcon.EDIT))
        self.menu_settings.addMenu(self.menu_mode)

        self.menu_rmchar = CheckableMenu('屏蔽字符', None, MenuIndicatorType.CHECK)
        self.menu_rmchar.addActions([self.ac_rm_space_c, self.ac_rm_endl_c, self.ac_rm_endl_s, self.ac_rm_newp, self.ac_rm_tab])
        self.menu_rmchar.setIcon(FluentIcon.icon(FluentIcon.FILTER))
        self.menu_settings.addMenu(self.menu_rmchar)

        self.menu_settings.addSeparator()
        # self.menu_settings.addWidget(self.spin_delay,False)
        # self.menu_settings.actions()[0].setIcon(FluentIcon.icon(FluentIcon.STOP_WATCH))
        # self.menu_settings.actions()[0].setIconText('字间延时：')
        # 邪修大法，addWidget会强制添加空icon间距，很丑
        self.menu_settings.addWidget(QWidget(size=QSize(200, 37), styleSheet='background-color:transparent;'), False)
        self.spin_word_delay.setParent(self.menu_settings)
        self.spin_word_delay.move(25, 80)
        self.menu_settings.addWidget(QWidget(size=QSize(200, 37), styleSheet='background-color:transparent;'), False)
        self.spin_paste_delay.setParent(self.menu_settings)
        self.spin_paste_delay.move(25, 120)

        # self.spin_delay.show()

        self.menu.addAction(self.ac_exit)
        self.setContextMenu(self.menu)

    def init_actions(self):
        self.ac_empty = QAction('(暂无记录)', enabled=False)
        self.ac_paste = QAction(FluentIcon.icon(FluentIcon.PASTE), '5s后粘贴', triggered=self.paste)
        self.ac_mode_wbw = QAction('逐字', checkable=True, checked=True, triggered=lambda: self.menu_mode.setActiveAction(self.menu_mode.actions()[0]))
        self.ac_mode_aao = QAction('整段', checkable=True, triggered=lambda: self.menu_mode.setActiveAction(self.menu_mode.actions()[1]))
        self.acgp_mode = QActionGroup(self)
        self.acgp_mode.addAction(self.ac_mode_wbw)
        self.acgp_mode.addAction(self.ac_mode_aao)
        self.ac_rm_space_c = QAction('连续空格', checkable=True, checked=True)
        self.ac_rm_endl_c = QAction(r'连续换行 (\n\n...)', checkable=True, checked=True)
        self.ac_rm_endl_s = QAction(r'单行换行 (\n)', checkable=True, checked=False)
        self.ac_rm_newp = QAction(r'换页 (\f)', checkable=True, checked=True)
        self.ac_rm_tab = QAction(r'制表/Tab (\t \v)', checkable=True, checked=True)
        self.spin_word_delay = MenuSpin('字间延迟：', 100, (10, 1000), 100)
        self.spin_paste_delay = MenuSpin('粘贴延迟：', 5000, (500, 10000), 500)
        self.spin_paste_delay.spin.valueChanged.connect(lambda v: self.ac_paste.setText(f"{v//1000}{'.'+str(v%1000//100) if v%1000 else ''}s后粘贴"))
        self.ac_exit = QAction(FluentIcon.icon(FluentIcon.CLOSE), '退出', triggered=app.exit)

    def update(self):
        temp = self.clipboard.text()
        self.setToolTip(f"{APP_NAME} v{APP_VERSION}\n当前模式：{'逐字模式'if self.ac_mode_wbw.isChecked() else '整段模式'}\n{temp.strip()}")
        if temp.strip():
            self.menu_history.removeAction(self.ac_empty)
            self.menu_history.addAction(QAction(temp.strip()[:30] + ('...'if len(temp.strip()) > 30 else ''), self, triggered=lambda txt=temp: self.paste(txt, True)))
            if len(self.menu_history.actions()) > 10:
                self.menu_history.removeAction(self.menu_history.actions()[0])

    def paste(self, txt='', paste_delayed=True):
        # txt留空则读取实时剪切板 
        def worker(txt):
            if txt:
                delay = self.spin_word_delay.value() if self.ac_mode_wbw.isChecked() else 0
                for i in txt:
                    keyboard.write(i)
                    if delay:
                        time.sleep(delay / 1000)
                    if keyboard.is_pressed('ctrl'):
                        break
        if not txt:
            txt = self.clipboard.text()
        if self.ac_rm_space_c.isChecked():
            txt = re.sub(r'\s+', ' ', txt)
        if self.ac_rm_endl_c.isChecked():
            txt = re.sub(r'\n+', '\n', txt)
        if self.ac_rm_endl_s.isChecked():
            txt = re.sub(r'\n', '', txt)
        if self.ac_rm_newp.isChecked():
            txt = re.sub(r'\f', '', txt)
        if self.ac_rm_tab.isChecked():
            txt = re.sub(r'\t|\v', '', txt)
        self.thread_paste = threading.Thread(target=worker, args=(txt,))
        QTimer.singleShot(self.spin_paste_delay.value() if paste_delayed else 0, self.thread_paste.start)


class MenuSpin(QWidget):
    def __init__(self, label: str, value: int, range: tuple[int, int], step: int):
        '''step为0时使用自动步长'''
        super().__init__()
        self.hbox = QHBoxLayout()
        self.label = BodyLabel(label)
        self.spin = CompactSpinBox()
        self.spin.setAccelerated(True)
        if step:
            self.spin.setSingleStep(step)
        else:
            self.spin.setStepType(CompactSpinBox.StepType.AdaptiveDecimalStepType)
        self.spin.setRange(*range)
        self.spin.setSuffix('ms')
        self.setValue(value)
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.spin, 1)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.label.setStyleSheet('QLabel{background-color:transparent;}')
        self.setLayout(self.hbox)
        self.setMaximumSize(175, 35)

    def setValue(self, value: int):
        self.spin.setValue(value)

    def value(self) -> int:
        return self.spin.value()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    theme_control.apply_theme(app, 'auto')
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setWindowIcon(QIcon('icon.png'))
    tray = SystemTray()
    sys.exit(app.exec())
