from PySide6.QtWidgets import QListWidgetItem, QTextEdit


class BaseMessageItem(QListWidgetItem):
    def __init__(self, message: str):
        super().__init__()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.set_message(message)

    def set_message(self, message: str):
        raise NotImplementedError("Subclasses should implement this method")


class UserMessageItem(BaseMessageItem):
    def set_message(self, message: str):
        self.text_edit.setHtml(f'<div style="border: 2px solid blue; padding: 5px;">{message}</div>')
        self.setSizeHint(self.text_edit.sizeHint())


class AssistantMessageItem(BaseMessageItem):
    def set_message(self, message: str):
        self.text_edit.setHtml(f'<div style="border: 2px solid green; padding: 5px;">{message}</div>')
        self.setSizeHint(self.text_edit.sizeHint())
