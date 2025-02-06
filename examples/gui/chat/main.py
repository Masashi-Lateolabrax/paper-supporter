import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QLabel
from PySide6.QtCore import Slot, Qt
from assistant_worker import AssistantWorker


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Application")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)

        self.message_input = QTextEdit(self)
        self.layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.loading_label = QLabel("Loading...", self)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setVisible(False)
        self.layout.addWidget(self.loading_label)

        self.worker = AssistantWorker("gpt-4o-mini")
        self.worker.assistant_reply.connect(self.on_finished)
        self.worker.start()

    @Slot()
    def send_message(self):
        user_message = self.message_input.toPlainText().strip()
        if user_message:
            self.chat_display.append(f"User: {user_message}")
            self.message_input.clear()
            self.worker.exec(user_message)
            self.loading_label.setVisible(True)

    @Slot(str)
    def on_finished(self, response: str):
        self.loading_label.setVisible(False)
        self.chat_display.append(f"Assistant: {response}")

    def closeEvent(self, event):
        self.worker.requestInterruption()
        self.worker.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
