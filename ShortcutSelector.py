from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from qfluentwidgets import *
import platform

# 强调色
ACCENT = themeColor()

# 计算派生颜色
ACCENT_HOVER = QColor(
    min(255, ACCENT.red() + 51),
    min(255, ACCENT.green() + 51),
    min(255, ACCENT.blue() + 51)
)
ACCENT_PRESSED = QColor(
    max(0, ACCENT.red() - 18),
    max(0, ACCENT.green() - 18),
    max(0, ACCENT.blue() - 18)
)
ACCENT_DARK = QColor(
    max(0, ACCENT.red() - 128),
    max(0, ACCENT.green() - 128),
    max(0, ACCENT.blue() - 128)
)
ACCENT_DARK_HOVER = QColor(
    max(0, ACCENT_DARK.red() + 17),
    max(0, ACCENT_DARK.green() + 17),
    max(0, ACCENT_DARK.blue() + 17)
)


class ShortcutKeyButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(28)
        self.setFixedHeight(28)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setStyleSheet(f"""
            ShortcutKeyButton {{
                background-color: {ACCENT.name()};
                color: #000000;
                border: none;
                border-radius: 8px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                font-size: 14px;
                font-weight: 500;
                padding: 0px 12px;
            }}
            ShortcutKeyButton:hover {{
                background-color: {ACCENT_HOVER.name()};
            }}
            ShortcutKeyButton:pressed {{
                background-color: {ACCENT_PRESSED.name()};
            }}
            ShortcutKeyButton:checked {{
                background-color: {ACCENT_DARK.name()};
                color: #FFFFFF;
            }}
            ShortcutKeyButton:checked:hover {{
                background-color: {ACCENT_DARK_HOVER.name()};
            }}
            """)


class ShortcutSelector(QWidget):
    shortcutChanged = Signal(QKeySequence)

    def __init__(self, require_modifier: bool = True, default_sequence: QKeySequence = QKeySequence(), parent=None):
        super().__init__(parent)
        self._require_modifier = require_modifier
        self._current_sequence = default_sequence
        self._is_editing = False

        system = platform.system()
        if system == "Darwin":
            self._meta_name = "⌘"
        elif system == "Windows":
            self._meta_name = "Win"
        else:
            self._meta_name = "Super"

        self._setup_ui()
        self._apply_styles()
        self._update_display()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFixedSize(250, 50)

    def _setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(8, 6, 8, 6)
        self.main_layout.setSpacing(8)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.container = QFrame()
        self.container.setObjectName("shortcutContainer")
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setContentsMargins(8, 4, 8, 4)
        self.container_layout.setSpacing(8)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.keys_layout = QHBoxLayout()
        self.keys_layout.setSpacing(4)

        self.ctrl_btn = ShortcutKeyButton()
        self.ctrl_btn.setText("Ctrl")

        self.shift_btn = ShortcutKeyButton()
        self.shift_btn.setText("Shift")

        self.alt_btn = ShortcutKeyButton()
        self.alt_btn.setText("Alt")

        self.meta_btn = ShortcutKeyButton()
        self.meta_btn.setText(self._meta_name)

        self.key_btn = ShortcutKeyButton()

        self.keys_layout.addWidget(self.ctrl_btn)
        self.keys_layout.addWidget(self.shift_btn)
        self.keys_layout.addWidget(self.alt_btn)
        self.keys_layout.addWidget(self.meta_btn)
        self.keys_layout.addWidget(self.key_btn)

        self.action_btn = QPushButton()
        self.action_btn.setObjectName("actionBtn")
        self.action_btn.setFixedSize(20, 20)
        self.action_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action_btn.setIcon(FluentIcon.icon(FluentIcon.EDIT))
        self.action_btn.setFlat(True)
        self.action_btn.clicked.connect(self._on_action_clicked)
        self.action_btn.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.container_layout.addLayout(self.keys_layout)
        self.container_layout.addStretch()
        self.container_layout.addWidget(self.action_btn)

        self.main_layout.addWidget(self.container)

    def _apply_styles(self):
        self.setStyleSheet(f"""
            ShortcutSelector {{
                background-color: transparent;
            }}
            #shortcutContainer {{
                background-color: transparent;
                border: 1px solid {'#3D3D3D'if isDarkTheme() else '#E0E0E0'};
                border-radius: 12px;
                min-width: 80px;
                min-height: 40px;
            }}
            #shortcutContainer:hover {{
                border: 1px solid {'#4D4D4D' if isDarkTheme() else '#D0D0D0'};
            }}
            #shortcutContainer[editing="true"] {{
                border: 1px solid {ACCENT.name()};
                background-color: #252525;
            }}
            #actionBtn {{
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 4px;
            }}
            #actionBtn:hover {{
                background-color: #3D3D3D;
            }}
            #actionBtn:pressed {{
                background-color: #4D4D4D;
            }}""")

    def _hide_all_keys(self):
        self.ctrl_btn.setVisible(False)
        self.shift_btn.setVisible(False)
        self.alt_btn.setVisible(False)
        self.meta_btn.setVisible(False)
        self.key_btn.setVisible(False)

    def _update_display(self):
        if self._current_sequence.isEmpty():
            self._hide_all_keys()
            return

        key_comb = self._current_sequence[0]
        modifiers = key_comb.keyboardModifiers()

        self.ctrl_btn.setVisible(bool(modifiers & Qt.KeyboardModifier.ControlModifier))
        self.shift_btn.setVisible(bool(modifiers & Qt.KeyboardModifier.ShiftModifier))
        self.alt_btn.setVisible(bool(modifiers & Qt.KeyboardModifier.AltModifier))
        self.meta_btn.setVisible(bool(modifiers & Qt.KeyboardModifier.MetaModifier))

        key_name = QKeySequence(key_comb.key()).toString()
        self.key_btn.setText(key_name if key_name else "?")
        self.key_btn.setVisible(True)
        self.key_btn.setChecked(False)

    def _on_action_clicked(self):
        self._current_sequence = QKeySequence()
        self.shortcutChanged.emit(self._current_sequence)
        self._stop_editing()

    def _start_editing(self):
        self._is_editing = True
        self._hide_all_keys()
        self.key_btn.setVisible(True)
        self.key_btn.setText("...")
        self.key_btn.setChecked(True)

        self.action_btn.setIcon(FluentIcon.icon(FluentIcon.CLOSE))
        self.action_btn.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        self.container.setProperty("editing", "true")
        self.container.style().unpolish(self.container)
        self.container.style().polish(self.container)

        self.setFocus(Qt.FocusReason.MouseFocusReason)
        self.grabKeyboard()

    def _stop_editing(self):
        self._is_editing = False
        self.releaseKeyboard()

        self.action_btn.setIcon(FluentIcon.icon(FluentIcon.EDIT))
        self.action_btn.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.container.setProperty("editing", "false")
        self.container.style().unpolish(self.container)
        self.container.style().polish(self.container)

        self._update_display()

    def _restore_prompt(self):
        if self._is_editing:
            self.key_btn.setText("...")

    def keyPressEvent(self, event: QKeyEvent):
        if not self._is_editing:
            super().keyPressEvent(event)
            return

        key = event.key()
        modifiers = event.modifiers()

        if key in (Qt.Key.Key_Control, Qt.Key.Key_Shift,
                   Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            return

        if key == Qt.Key.Key_Escape:
            self._stop_editing()
            return

        if self._require_modifier:
            has_modifier = bool(modifiers & (
                Qt.KeyboardModifier.ControlModifier |
                Qt.KeyboardModifier.ShiftModifier |
                Qt.KeyboardModifier.AltModifier |
                Qt.KeyboardModifier.MetaModifier
            ))
            if not has_modifier:
                self.key_btn.setText("需要修饰键")
                QTimer.singleShot(1000, self._restore_prompt)
                return

        self._current_sequence = QKeySequence(QKeyCombination(modifiers, Qt.Key(key)))
        self.shortcutChanged.emit(self._current_sequence)
        self._stop_editing()

    def keyReleaseEvent(self, event: QKeyEvent):
        if not self._is_editing:
            super().keyReleaseEvent(event)

    def focusOutEvent(self, event):
        if self._is_editing:
            self._stop_editing()
        super().focusOutEvent(event)

    def mousePressEvent(self, event):
        if not self._is_editing and event.button() == Qt.MouseButton.LeftButton:
            self._start_editing()
        super().mousePressEvent(event)
        event.accept()

    def shortcut(self) -> QKeySequence:
        return self._current_sequence

    def setShortcut(self, sequence: QKeySequence):
        self._current_sequence = sequence
        self._update_display()

    def setRequireModifier(self, require: bool):
        self._require_modifier = require

    def isRequireModifier(self) -> bool:
        return self._require_modifier


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    demo = ShortcutSelector()
    demo.show()
    sys.exit(app.exec())
