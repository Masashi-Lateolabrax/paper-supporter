import markdown
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QTextEdit, QSizePolicy


class BaseMessageItem(QListWidgetItem):
    def __init__(self):
        super().__init__()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.adjust_height()

    def adjust_height(self):
        self.text_edit.document().setTextWidth(self.text_edit.viewport().width())
        self.setSizeHint(self.text_edit.document().size().toSize())


class UserMessageItem(BaseMessageItem):
    def __init__(self, message: str):
        super().__init__()
        self.set_message(message)

    def set_message(self, message: str):
        html_message = markdown.markdown(message)
        self.text_edit.setHtml(f'<div style="border: 2px solid blue; padding: 5px;">{html_message}</div>')
        self.adjust_height()


class AssistantMessageItem(BaseMessageItem):
    def __init__(self):
        super().__init__()
        self.content = []

    def append_delta(self, delta: str):
        self.content.append(delta)
        html_message = markdown.markdown("".join(self.content))
        self.text_edit.setHtml(f'<div style="border: 2px solid green; padding: 5px;">{html_message}</div>')
        self.adjust_height()
