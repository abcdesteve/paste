from .progress_popup_ui import Ui_progress_popup
from .input_dialog_ui import Ui_input_dialog

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qfluentwidgets.components.dialog_box.mask_dialog_base import MaskDialogBase
from qfluentwidgets import *

import os
import logging
import time
from PIL import Image
import pillow_heif
pillow_heif.register_heif_opener()


def benchmark(fx):
    def wrapper(*args, **kwargs):
        start = time.time_ns()
        fx(*args, **kwargs)
        end = time.time_ns()
        print(f'函数{fx.__name__}消耗{(end-start)/1000000}ms\n')
    return wrapper


class sltk:
    "神龙工具集"

    def scan_file(dir_name: str, goal: str, depth: int, strict: bool = True, black_list: list[str] = ['C:\\Windows', 'C:\\$RECYCLE.BIN', 'C:\\Recovery', 'C:\\System Volume Information', 'D:\\$RECYCLE.BIN', 'D:\\System Volume Information']) -> list[str]:
        """
        Find the goal in the given dir.
        Return mutiple results if found.

        argvs:
            dir: The location to scan.
            goal: The file to be found.
            depth: Decide how many folders to be scan.  1 means no child folder is scaned
            strict: If True, only return the exact match.
            black_list: Jump through to save time

        e.g. scan_file('C:\\ ','python.exe',5)
        >>> ["C:\\user\\abcdesteve\\python\\python.exe","C:\\python\\python.exe"]
        """
        results = []
        if os.path.isdir(dir_name) and depth > 0 and dir_name not in black_list:
            try:
                lis = os.listdir(dir_name)
                if strict:
                    if goal in lis:
                        results.append(sltk.join_path(dir_name, goal))
                else:
                    for i in lis:
                        if goal in i:
                            results.append(sltk.join_path(dir_name, i))
                temp = [results.extend(sltk.scan_file(sltk.join_path(dir_name, i), goal, depth - 1, strict, black_list))
                        for i in lis if os.path.isdir(sltk.join_path(dir_name, i))]
                # print(f'temp:{temp}')
                return results
            except PermissionError:
                logging.warning(
                    f"Not enough permission when trying to scan dir: {dir_name}")
                return []
        else:
            return []

    def safe_load(origin: dict[str, int | str | dict], data: dict[str, int | str | dict]) -> dict[str, int | str | dict]:
        '''安全加载json配置，避免因版本不同导致配置冲突'''
        temp={}
        for okey, ovalue in origin.items():
            if okey in list(data.keys()):
                if type(ovalue) == dict:
                    temp[okey] = sltk.safe_load(sltk, ovalue, data[okey])
                else:
                    temp[okey] = data[okey]
            else:
                temp[okey]=ovalue
        return temp

    def unique_add_items(widget: QComboBox | ComboBox | QListWidget | ListWidget, *items: str | list[str], format_item: bool = True):
        '''为ComboBox/ListWidget不重复地添加一个或多个item，同时格式化路径（如果可以）'''
        previous_items = [(widget.itemText(i) if type(widget) in [
                           QComboBox, ComboBox]else widget.item(i).text()) for i in range(widget.count())]
        if type(items[0]) == list:
            items = items[0]
        for i in items:
            if format_item:
                i = os.path.normpath(i)
            if i not in previous_items:
                widget.addItem(i)

    def unique_set_items(widget: QComboBox | ComboBox, *items: str | list[str], format_item: bool = True):
        '''先清空ComboBox，再运行 `sltk.unique_add_items` ，并尝试恢复原来的选项'''
        previous_txt = widget.currentText()
        widget.clear()
        sltk.unique_add_items(widget, *items, format_item=format_item)
        lis = sltk.expend_children_text(widget)
        if previous_txt in lis:
            widget.setCurrentText(previous_txt)
        else:
            widget.setCurrentIndex(0)

    def join_path(*argv: str) -> str:
        return os.path.normpath(os.path.join(*argv))

    def split_path(path: str) -> list[str]:
        path = os.path.normpath(path)
        result = []
        while True:
            path, temp = os.path.split(path)
            if temp:
                result.insert(0, temp)
            else:
                if path:  # 注意传入相对路径（无盘符时）path可能为空
                    result.insert(0, path)
                break
        return result

    def expend_children_text(widget: QComboBox | QListWidget | QTableWidget | QTreeWidget | ComboBox | ListWidget | TableWidget | TreeWidget) -> list[str] | list[list[str]]:
        '''
        Return all item text in the widget\n
        `ComboBox` -> list[str]\n
        `ListWidget` -> list[str]\n
        `TableWidget` -> list[list[str]]\n
        `TreeWidget` -> list[list[str]]]
        '''
        # if type(widget) in [QComboBox, ComboBox]:
        if isinstance(widget, (QComboBox, ComboBox, EditableComboBox)):
            return [widget.itemText(i) for i in range(widget.count())]

        # elif type(widget) in [QListWidget, ListWidget]:
        elif isinstance(widget, (QListWidget, ListWidget)):
            return [widget.item(i)for i in range(widget.count())]

        # elif type(widget) in [QTableWidget, TableWidget,]:
        elif isinstance(widget, (QTableWidget, TableWidget)):
            return [
                [widget.item(row, col).text()
                 for col in range(widget.columnCount())]
                for row in range(widget.rowCount())]

        # elif type(widget) in [QTreeWidget, TreeWidget]:
        elif isinstance(widget, (QTreeWidget, TreeWidget)):
            return [[widget.topLevelItem(i).text(col) for col in range(widget.columnCount())] for i in range(widget.topLevelItemCount())]
        else:
            raise TypeError(f'Unsupported widget type: {type(widget)}')

    def bit2size(bit: int | str) -> str:
        '为字节自动匹配单位'
        bit = int(bit)
        for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']:
            if bit < 1024:
                return f"{bit:.2f} {unit}"
            bit /= 1024.0

    def calc_hash(file: str, md5: bool = False, crc32: bool = False, blake3: bool = False, sha1: bool = False, sha224: bool = False, sha256: bool = False, sha384: bool = False, sha512: bool = False, buffer_size: int = 1024 * 1024) -> dict[str, str]:
        import hashlib
        from zlib import crc32 as calc_crc32
        import blake3 as blake3lib
        '计算文件的哈希值'
        result = {}
        _md5, _crc32, _blake3, _sha1, _sha224, _sha256, _sha384, _sha512 = hashlib.md5(), 0, blake3lib.blake3(
        ), hashlib.sha1(), hashlib.sha224(), hashlib.sha256(), hashlib.sha384(), hashlib.sha512()
        with open(file, 'rb') as f:
            while True:
                temp = f.read(buffer_size)
                if not temp:
                    break
                if md5:
                    _md5.update(temp)
                if crc32:
                    _crc32 = calc_crc32(temp, _crc32)  # 用zlib的比binascii更快
                if blake3:
                    _blake3.update(temp)
                if sha1:
                    _sha1.update(temp)
                if sha224:
                    _sha224.update(temp)
                if sha256:
                    _sha256.update(temp)
                if sha384:
                    _sha384.update(temp)
                if sha512:
                    _sha512.update(temp)

        if md5:
            result['md5'] = _md5.hexdigest().upper()
        if crc32:
            result['crc32'] = hex(_crc32)[2:].upper()
        if blake3:
            result['blake3'] = _blake3.hexdigest().upper()
        if sha1:
            result['sha1'] = _sha1.hexdigest().upper()
        if sha224:
            result['sha224'] = _sha224.hexdigest().upper()
        if sha256:
            result['sha256'] = _sha256.hexdigest().upper()
        if sha384:
            result['sha384'] = _sha384.hexdigest().upper()
        if sha512:
            result['sha512'] = _sha512.hexdigest().upper()
        return result


class QMessageBox:
    """
    窗口类型支持 `information` | `warning` | `question`

    `mask` 指定窗口是否有遮罩
    """

    Yes = True
    No = False

    def base(parent, title, content, mask=False):
        if mask:
            widget = MessageBox(title, content, parent)
        else:
            # Dialog不支持圆角
            widget = Dialog(title, content, parent)
            widget.setTitleBarVisible(False)
            # MessageBox不支持关闭遮罩
            # widget = MessageBox(title, content, parent)
            # widget.clearMask()
        widget.buttonLayout.setDirection(QBoxLayout.Direction.RightToLeft)  # 把确认按钮放右边
        widget.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        return widget

    def information(parent: QMainWindow, title, content, mask=True, text='OK') -> None:
        widget = QMessageBox.base(parent, title, content, mask)

        widget.cancelButton.hide()

        widget.yesButton.setShortcut('alt+y')
        widget.yesButton.setText(text)

        widget.exec()

    def warning(parent: QMainWindow, title, content, mask=True, text='OK') -> None:
        widget = QMessageBox.base(parent, title, content, mask)

        # widget.yesButton.setStyleSheet('color:#ff0000')
        logging.debug("unfinished")
        widget.cancelButton.hide()

        widget.yesButton.setShortcut('alt+y')
        widget.yesButton.setText(text)

        widget.exec()

    def question(parent: QMainWindow, title, content, mask=True, yes_text='继续', no_text='取消') -> bool:
        widget = QMessageBox.base(parent, title, content, mask)

        widget.yesButton.setShortcut('Alt+Y, Enter, Return')
        widget.cancelButton.setShortcut('Alt+N, Escape')
        widget.yesButton.setText(yes_text)
        widget.cancelButton.setText(no_text)

        return QMessageBox.Yes if widget.exec() else QMessageBox.No


class InputDialog(MaskDialogBase, Ui_input_dialog):
    def __init__(self):
        pass

    def run(self, parent, title: str, content: str, options: list[str] = [], editable: bool = True) -> str:
        '''
        Receive an optional argv `options` which will be shown in the `ComboBox`\n
        Return input txt
        '''
        super().__init__(parent)
        self.setupUi(self.widget)
        FluentStyleSheet.DIALOG.apply(self)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        # self.btn_cancel.setShortcut('Alt+N, Escape')
        # self.shortcut_cancel = QShortcut('Alt+N, Escape', self, self.cancel, Qt.ShortcutContext.ApplicationShortcut)
        # self.btn_ok.setShortcut('Alt+Y, Enter, Return')
        # self.shortcut_ok = QShortcut('Alt+Y, Enter, Return', self, self.ok, Qt.ShortcutContext.ApplicationShortcut)
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_ok.clicked.connect(self.ok)
        self.title.setText(title)
        self.content.setText(content)
        sltk.unique_add_items(self.comboBox, options, format_item=False)
        self.comboBox.dropButton.setVisible(bool(len(options)))
        self.comboBox.setReadOnly(not editable)
        self.comboBox.setFocus()
        self.status = False
        # self.show()
        self.exec()
        return self.comboBox.currentText() if self.status else None

    def cancel(self):
        self.status = False
        self.close()

    def ok(self):
        self.status = True
        self.close()

    # def closeEvent(self, arg: QCloseEvent):
    #     self.done(1)


class StatisticsWidget(QWidget):
    """ 状态数值对应组件 """

    def __init__(self, title: str, value: str = '未知', parent=None):
        super().__init__(parent=parent)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.valueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vBoxLayout.setContentsMargins(5, 0, 5, 0)
        self.vBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignBottom)

        setFont(self.valueLabel, 18, QFont.DemiBold)
        self.titleLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))

    def setTitle(self, title: str = ''):
        self.titleLabel.setText(str(title))

    def setValue(self, value: str = '未知'):
        self.valueLabel.setText(str(value))


class ProgressPopUp(MaskDialogBase, Ui_progress_popup):
    """进度弹窗（不阻塞）\n
    配合_auto_update机制，可在不同线程中更新进度，注意变量为单向同步，不应读取\n
    `title` 弹窗标题
    `total` 总进度（不传递时使用不确定的进度条） e.g. 100
    `delay` 延迟显示进度条（ms），伪装加载动画
    `show_time` 是否显示预估时间\n
    `current` 实时状态 e.g. C:/Users/xxx/Downloads/a.txt\n
    `progress` 实时进度（仅在传递`total`时有效） e.g. 50\n
    `thumbnail` 显示缩略图\n
    `processed` 已处理数（仅在传递`total`时有效） e.g. 50
    """

    def __init__(self):
        self.total = 0
        self.title = ""
        self.currentItem = ""
        self.thumbnail = ""
        self.processed = -1
        self.is_done = False

        self._total = 0
        self._title = ""
        self._currentItem = ""
        self._thumbnail = ""
        self._processed = -1

    def _auto_update(self):
        if self.total != self._total:
            self.setTotal(self.total)
            self._total = self.total
        if self.title != self._title:
            self.setTitle(self.title)
            self._title = self.title
        if self.currentItem != self._currentItem:
            self.setCurrentItem(self.currentItem)
            self._currentItem = self.currentItem
        if self.thumbnail != self._thumbnail:
            self.setThumbnail(self.thumbnail)
            self._thumbnail = self.thumbnail
        if self.processed != self._processed:
            self.setProcessed(self.processed)
            self._processed = self.processed
        if self.is_done:
            self.timer.stop()
            QTimer.singleShot(0, lambda: QMessageBox.information(self.mainwindow, *self.done_msg))
            self.close()

    def run(self, parent, title: str, done_msg: list[str, str] = ['处理完成', ''], total: int = 0, delay: int = 1000, show_time=True):
        super().__init__(parent)
        self.mainwindow = parent
        self.done_msg = done_msg
        self.setupUi(self.widget)
        FluentStyleSheet.DIALOG.apply(self)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        self.label_title.setText(title)

        self.setTotal(0)
        if total:  # 可能出现计算total很快，delay之后覆盖原值的情况
            QTimer().singleShot(delay, lambda: self.setTotal(total))

        self.label_time_left.setVisible(show_time)

        self.start_time = self.stage_time = time.time()

        self.timer = QTimer(interval=1000)
        self.timer.timeout.connect(self._auto_update)
        self.timer.timeout.connect(self._updateTime)
        self.timer.start()

        QTimer().singleShot(0, self.exec)
        return self

    def setTotal(self, value: int):
        self.label_progress.setVisible(value != 0)
        self.label_progress_data.setVisible(value != 0)

        self.ProgressBar.setVisible(value != 0)
        self.IndeterminateProgressBar.setVisible(value == 0)
        return self

    def setTitle(self, txt: str = ""):
        self.label_title.setText(txt)

    def setCurrentItem(self, txt: str = ""):
        "当前处理的项目/文件，不是进度"
        # self.label_current.setVisible(value == "")
        self.label_current.setText(txt)
        return self

    def setThumbnail(self, thumbnail: str = None):
        try:
            with Image.open(thumbnail) as img:
                self.ImageLabel.setPixmap(img.toqpixmap().scaled(
                    75, 75, Qt.AspectRatioMode.KeepAspectRatio))
        except:
            self.ImageLabel.setPixmap(QPixmap())
        return self

    def setProcessed(self, value: int):
        "`value`为当前实时进度，不是百分比\n\n需要设置`total`"
        if self.total:
            percentage = value / self.total * 100
        else:
            percentage = 0
        self.label_progress_data.setText('%.1f%% (%d/%d)' % (percentage, value, self.total))
        self.ProgressBar.setValue(int(percentage))
        return self

    def new_stage(self):
        self.stage_time = time.time()

    def _updateTime(self):
        def format_time(seconds: int | float):
            if seconds <= 0:
                return '正在计算'
            if seconds > 60 * 60 * 24:
                return "超过1天"
            h = seconds // 3600
            seconds %= 3600
            m = seconds // 60
            seconds %= 60
            seconds = int(seconds)
            if h:
                return '%02d:%02d:%02d' % (h, m, seconds)
            if m:
                return '%02d:%02d' % (m, seconds)
            return f'{seconds}s'

        self.label_time_past.setText('已用时间：' + format_time(time.time() - self.start_time))
        if self.processed * self.total != 0:
            past_time = time.time() - self.stage_time
            left_time = past_time / (self.processed / self.total) - past_time
            self.label_time_left.setText('剩余时间：' + format_time(left_time))


class MyFluentIcon(FluentIconBase, Enum):

    def path(self, theme=Theme.AUTO) -> str:
        return sltk.join_path(os.path.dirname(__file__), 'icons', f'{self.value}_{getIconColor(theme)}.svg')
        # return f'{os.path.dirname(__file__)}icons/{self.value}'
