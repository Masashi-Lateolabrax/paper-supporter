from openai.types import FileObject
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QLabel, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from paper_supporter.lib.openai.file_manager import FileManager


class StorageManager:
    def __init__(self, file_manager: FileManager, parent: QWidget):
        self.file_manager = file_manager
        self.parent = parent
        self.layout = QVBoxLayout()

        self._initialize_ui()
        self._connect_signals()

    def _initialize_ui(self):
        self.storage_label = QLabel("Storage", self.parent)
        self.storage_label.setAlignment(Qt.AlignCenter)
        self.storage_label.setStyleSheet("text-decoration: underline;")
        self.layout.addWidget(self.storage_label)

        self.storage_display = QListWidget(self.parent)
        self.layout.addWidget(self.storage_display)

        self.upload_button = QPushButton("upload", self.parent)
        self.remove_button = QPushButton("remove", self.parent)
        self.upload_remove_layout = QHBoxLayout()
        self.upload_remove_layout.addWidget(self.upload_button)
        self.upload_remove_layout.addWidget(self.remove_button)
        self.layout.addLayout(self.upload_remove_layout)

    def _connect_signals(self):
        self.upload_button.clicked.connect(self.parent.upload_file)
        self.remove_button.clicked.connect(self.parent.remove_file)

    def update_storage_display(self):
        self.storage_display.clear()
        attached_files = {file.id for file in self.file_manager.get_attached_files()}
        for file in self.file_manager.get_files():
            if file.id not in attached_files:
                if not self.storage_display.findItems(file.filename, Qt.MatchExactly):
                    item = QListWidgetItem(file.filename)
                    item.setData(Qt.UserRole, file)
                    self.storage_display.addItem(item)

    def upload_file(self, file_path):
        self.set_buttons_state(False, "uploading...")
        with open(file_path, 'rb') as f:
            file: FileObject = self.file_manager.upload_file(f)
            self.update_storage_display()
            print(f"Uploaded file: {file.id}")
        self.set_buttons_state(True)

    def remove_file(self, item: QListWidgetItem):
        self.set_buttons_state(False, "removing...")
        file: FileObject = item.data(Qt.UserRole)
        if self.file_manager.remove_file(file):
            self.storage_display.takeItem(self.storage_display.row(item))
            print(f"Removed file: {file.id}")
        else:
            print(f"Failed to remove file: {file.id}")
        self.set_buttons_state(True)

    def set_buttons_state(self, enabled, action=None):
        self.upload_button.setText(action if not enabled else "upload")
        self.remove_button.setText(action if not enabled else "remove")
        self.upload_button.setEnabled(enabled)
        self.remove_button.setEnabled(enabled)

        vector_store_manager = self.parent.vector_store_manager
        vector_store_manager.attach_button.setText(action if not enabled else "attach")
        vector_store_manager.detach_button.setText(action if not enabled else "detach")
        vector_store_manager.attach_button.setEnabled(enabled)
        vector_store_manager.detach_button.setEnabled(enabled)
