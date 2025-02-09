from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from .chat import ChatWidget
from .file_manager import FileWidget
from ..prerude import ASSISTANT_VECTOR_STORE_ID


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat and File Manager")
        self.setGeometry(100, 100, 1200, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        self._initialize_windows()

    def _initialize_windows(self):
        self.chat_widget = ChatWidget()
        self.file_widget = FileWidget()

        self.main_layout.addWidget(self.chat_widget)
        self.main_layout.addWidget(self.file_widget)

    def closeEvent(self, event):
        if self.chat_widget.worker:
            self.chat_widget.worker.requestInterruption()
            self.chat_widget.worker.wait()
        ASSISTANT_VECTOR_STORE_ID.set(self.file_widget.vector_store_manager.vector_store_id)
        event.accept()
