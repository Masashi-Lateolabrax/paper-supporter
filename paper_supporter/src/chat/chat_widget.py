import markdown
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from paper_supporter.prerude import ASSISTANT_VECTOR_STORE_ID
from paper_supporter.src.chat.assistant_worker import AssistantWorker


class ChatWidget(QWidget):
    user_message = Signal(str)  # Define the signal

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Application")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout(self)

        self._initialize_ui()

        vector_store_id = ASSISTANT_VECTOR_STORE_ID.get()
        self.worker = AssistantWorker("gpt-4o-mini", vector_store_id)
        self.worker.assistant_reply.connect(self.on_finished)
        self.user_message.connect(self.worker.receive_message)
        self.worker.start()

    def _initialize_ui(self):
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
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
            self.chat_display.append(f"<b>User:</b> {user_message}")
            self.message_input.clear()
            self.send_button.setEnabled(False)
            self.user_message.emit(user_message)  # Emit the signal
            self.loading_label.setVisible(True)

    @Slot(str)
    def on_finished(self, response: str):
        self.loading_label.setVisible(False)
        self.send_button.setEnabled(True)
        html_response = markdown.markdown(response)
        self.chat_display.append(f"<b>Assistant:</b> {html_response}")

    def closeEvent(self, event):
        self.worker.requestInterruption()
        self.worker.wait()
        event.accept()
