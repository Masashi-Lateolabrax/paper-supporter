import enum

from PySide6.QtCore import Qt, Signal, Slot, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QListWidget, QAbstractItemView

from paper_supporter.prerude import ASSISTANT_VECTOR_STORE_ID

from .assistant_worker import AssistantWorker
from .message_item import UserMessageItem, ProgressedMessageItem, AssistantMessageItem


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
        self.worker.assistant_text_delta.connect(self.on_html)
        self.worker.message_complete.connect(self.finalize_message)
        self.user_message.connect(self.worker.receive_message)
        self.worker.start()

        self.debounce_timer = QTimer(self)
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.process_debounced_html)
        self.pending_html_message = ""
        self.timer_running = False

    def _initialize_ui(self):
        self.chat_display = QListWidget(self)
        self.chat_display.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
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
    def on_html(self, html_message: str):
        self.pending_html_message = html_message
        if not self.timer_running:
            self.debounce_timer.start(100)  # 100ms debounce time
            self.timer_running = True

    @Slot()
    def process_debounced_html(self):
        self.timer_running = False
        last_item = self.chat_display.item(self.chat_display.count() - 1)
        if isinstance(last_item, ProgressedMessageItem):
            last_item.set_message(self.pending_html_message)
        else:
            width = self.chat_display.width()
            item = ProgressedMessageItem(self.pending_html_message, width)
            self.chat_display.addItem(item)
            self.chat_display.setItemWidget(item, item.label)

    @Slot()
    def finalize_message(self):
        last_item = self.chat_display.item(self.chat_display.count() - 1)
        if isinstance(last_item, ProgressedMessageItem):
            self.chat_display.takeItem(self.chat_display.row(last_item))
            self.add_message(last_item.label.text(), SenderType.ASSISTANT)
            self.loading_label.setVisible(False)
            self.send_button.setEnabled(True)

    def add_message(self, message: str, sender: SenderType):
        visible_width = self.chat_display.viewport().width()
        if sender == SenderType.USER:
            item = UserMessageItem(message, visible_width)
            self.chat_display.addItem(item)
            self.chat_display.setItemWidget(item, item.text_edit)
        else:
            item = AssistantMessageItem(message, visible_width)
            self.chat_display.addItem(item)
            self.chat_display.setItemWidget(item, item.text_edit)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        visible_width = self.chat_display.viewport().width()
        for index in range(self.chat_display.count()):
            item = self.chat_display.item(index)
            if isinstance(item, (UserMessageItem, AssistantMessageItem)):
                item.adjust_height(visible_width)
        self.chat_display.updateGeometry()

    def closeEvent(self, event):
        self.worker.requestInterruption()
        self.worker.wait()
        event.accept()
