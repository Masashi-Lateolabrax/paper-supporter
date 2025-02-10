from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from paper_supporter.lib.utils import EnvVariable

from .chat import ChatWidget
from .file_manager import FileWidget


class MainWindow(QMainWindow):
    def __init__(self, env_variable: EnvVariable):
        super().__init__()
        self.env = env_variable

        self.setWindowTitle("Chat and File Manager")
        self.setGeometry(100, 100, 1200, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        self._initialize_windows()

    def _initialize_windows(self):
        self.chat_widget = ChatWidget(self.env)

        self.file_widget = FileWidget(self.env)
        self.file_widget.setFixedWidth(300)

        self.main_layout.addWidget(self.chat_widget)
        self.main_layout.addWidget(self.file_widget)

    def closeEvent(self, event):
        if self.chat_widget.worker:
            self.chat_widget.worker.requestInterruption()
            self.chat_widget.worker.wait()
        self.env.set_vector_store_id(self.file_widget.vector_store_manager.vector_store_id)
        event.accept()
