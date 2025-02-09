from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QTextEdit, QLabel, QSizePolicy


class UserMessageItem(QListWidgetItem):
    def __init__(self, message: str, width):
        super().__init__()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._set_message(message)
        self.adjust_height(width)

    def _set_message(self, message: str):
        self.text_edit.setHtml(f'<div style="padding: 5px;">User: <br> {message}</div>')

    def adjust_height(self, width=None):
        if width is None:
            width = self.text_edit.viewport().width()
        self.text_edit.setFixedWidth(width)
        self.text_edit.document().setTextWidth(width)
        self.text_edit.setFixedHeight(self.text_edit.document().size().height())
        self.setSizeHint(self.text_edit.size())
        self.text_edit.updateGeometry()


class ProgressedMessageItem(QListWidgetItem):
    def __init__(self, html_message, width):
        super().__init__()

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.label.setWordWrap(True)
        self.label.setVisible(True)

        self.label.setFixedWidth(width)

        self.set_message(html_message)

    def set_message(self, html_message: str):
        self.label.setText(f'<div style="padding: 5px;">Assistant: <br> {html_message}</div>')
        self._adjust_height()

    def _adjust_height(self):
        self.label.adjustSize()
        self.setSizeHint(self.label.size())


class AssistantMessageItem(QListWidgetItem):
    def __init__(self, html_message: str, width):
        super().__init__()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._set_message(html_message)
        self.adjust_height(width)

    def _set_message(self, html_message: str):
        self.text_edit.setHtml(html_message)

    def adjust_height(self, width=None):
        if width is None:
            width = self.text_edit.viewport().width()
        self.text_edit.setFixedWidth(width)
        self.text_edit.document().setTextWidth(width)
        self.text_edit.setFixedHeight(self.text_edit.document().size().height())
        self.setSizeHint(self.text_edit.size())
        self.text_edit.updateGeometry()
