from openai.types import FileObject

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QLabel, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout, QWidget

from paper_supporter.lib.openai.file_manager import FileManager
from storage_manager import StorageManager


class VectorStoreManager:
    def __init__(self, file_manager: FileManager, parent: QWidget):
        self.file_manager = file_manager
        self.parent = parent
        self.layout = QVBoxLayout()

        self.vector_store_label = QLabel("Vector Store", parent)
        self.vector_store_label.setAlignment(Qt.AlignCenter)
        self.vector_store_label.setStyleSheet("text-decoration: underline;")
        self.layout.addWidget(self.vector_store_label)

        self.vector_store_display = QListWidget(parent)
        self.layout.addWidget(self.vector_store_display)

        self.attach_button = QPushButton("attach", parent)
        self.detach_button = QPushButton("detach", parent)
        self.attach_detach_layout = QHBoxLayout()
        self.attach_detach_layout.addWidget(self.attach_button)
        self.attach_detach_layout.addWidget(self.detach_button)
        self.layout.addLayout(self.attach_detach_layout)

        self.attach_button.clicked.connect(parent.attach_file)
        self.detach_button.clicked.connect(parent.detach_file)

    def update_vector_store_display(self):
        self.vector_store_display.clear()
        files = self.file_manager.get_attached_files()
        for f in files:
            storage_file = next((x for x in self.file_manager.get_files() if x.id == f.id), None)
            if not storage_file:
                continue
            item = QListWidgetItem(storage_file.filename)
            item.setData(Qt.UserRole, storage_file)
            self.vector_store_display.addItem(item)

    def attach_file(self, item: QListWidgetItem):
        self.set_buttons_state(False, "attaching...")
        file: FileObject = item.data(Qt.UserRole)
        if self.file_manager.attach_file(file):
            new_item = QListWidgetItem(file.filename)
            new_item.setData(Qt.UserRole, file)
            self.vector_store_display.addItem(new_item)
            self.parent.storage_manager.storage_display.takeItem(self.parent.storage_manager.storage_display.row(item))
            print(f"Attached file: {file.id}")
        else:
            print(f"Failed to attach file: {file.id}")
        self.set_buttons_state(True)

    def detach_file(self, item: QListWidgetItem):
        self.set_buttons_state(False, "detaching...")
        file: FileObject = item.data(Qt.UserRole)
        if self.file_manager.detach_file(file):
            new_item = QListWidgetItem(file.filename)
            new_item.setData(Qt.UserRole, file)
            self.vector_store_display.takeItem(self.vector_store_display.row(item))
            self.parent.storage_manager.storage_display.addItem(new_item)
            print(f"Detached file: {file.id}")
        else:
            print(f"Failed to detach file: {file.id}")
        self.set_buttons_state(True)

    def set_buttons_state(self, enabled, action=None):
        if enabled:
            self.attach_button.setText("attach")
            self.detach_button.setText("detach")
            self.parent.storage_manager.upload_button.setText("upload")
            self.parent.storage_manager.remove_button.setText("remove")
        else:
            self.attach_button.setText(action)
            self.detach_button.setText(action)
            self.parent.storage_manager.upload_button.setText(action)
            self.parent.storage_manager.remove_button.setText(action)

        self.attach_button.setEnabled(enabled)
        self.detach_button.setEnabled(enabled)
        self.parent.storage_manager.upload_button.setEnabled(enabled)
        self.parent.storage_manager.remove_button.setEnabled(enabled)
