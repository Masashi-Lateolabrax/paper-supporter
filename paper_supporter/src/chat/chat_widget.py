import enum

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QListWidget

from paper_supporter.prerude import ASSISTANT_VECTOR_STORE_ID

from .assistant_worker import AssistantWorker
from .message_item import UserMessageItem, AssistantMessageItem


class SenderType(enum.Enum):
    USER = 1
    ASSISTANT = 2


class ChatWidget(QWidget):
    user_message = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Application")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout(self)

        self._initialize_ui()

        vector_store_id = ASSISTANT_VECTOR_STORE_ID.get()
        self.worker = AssistantWorker("gpt-4o-mini", vector_store_id)
        self.worker.assistant_text_delta.connect(self.on_text_delta)
        self.user_message.connect(self.worker.receive_message)
        self.worker.start()

    def _initialize_ui(self):
        self.chat_display = QListWidget(self)
        self.layout.addWidget(self.chat_display)

        self.message_input = QTextEdit(self)
        self.message_input.setFixedHeight(150)
        self.layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.loading_label = QLabel("Loading...", self)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setVisible(False)
        self.layout.addWidget(self.loading_label)

    @Slot()
    def send_message(self):
        user_message = self.message_input.toPlainText().strip()
        if user_message:
            self.add_message(user_message, SenderType.USER)
            self.message_input.clear()
            self.send_button.setEnabled(False)
            self.user_message.emit(user_message)
            self.loading_label.setVisible(True)

    @Slot(str)
    def on_text_delta(self, delta: str):
        last_item = self.chat_display.item(self.chat_display.count() - 1)
        if isinstance(last_item, AssistantMessageItem):
            last_item.append_delta(delta)
            last_item.adjust_height()
        else:
            self.add_message(delta, SenderType.ASSISTANT)
            self.loading_label.setVisible(False)
            self.send_button.setEnabled(True)

    def add_message(self, message: str, sender: SenderType):
        if sender == SenderType.USER:
            item = UserMessageItem(message)
        else:
            item = AssistantMessageItem()
            item.append_delta(message)
        self.chat_display.addItem(item)
        self.chat_display.setItemWidget(item, item.text_edit)

    def closeEvent(self, event):
        self.worker.requestInterruption()
        self.worker.wait()
        event.accept()
