from openai.types import FileObject
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QLabel, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from paper_supporter.lib.openai.file_manager import FileManager


class VectorStoreManager:
    def __init__(self, file_manager: FileManager, parent: QWidget, vector_store_id: str = None):
        self.file_manager = file_manager
        self.parent = parent
        self.vector_store_id = vector_store_id
        self.layout = QVBoxLayout()

        self._initialize_ui()
        self._connect_signals()

    def _initialize_ui(self):
        self.vector_store_label = QLabel("Vector Store", self.parent)
        self.vector_store_label.setAlignment(Qt.AlignCenter)
        self.vector_store_label.setStyleSheet("text-decoration: underline;")
        self.layout.addWidget(self.vector_store_label)

        self.vector_store_display = QListWidget(self.parent)
        self.layout.addWidget(self.vector_store_display)

        self.attach_button = QPushButton("attach", self.parent)
        self.detach_button = QPushButton("detach", self.parent)
        self.attach_detach_layout = QHBoxLayout()
        self.attach_detach_layout.addWidget(self.attach_button)
        self.attach_detach_layout.addWidget(self.detach_button)
        self.layout.addLayout(self.attach_detach_layout)

    def _connect_signals(self):
        self.attach_button.clicked.connect(self.parent.attach_file)
        self.detach_button.clicked.connect(self.parent.detach_file)

    def update_vector_store_display(self):
        self.vector_store_display.clear()
        files = self.file_manager.get_attached_files()
        for f in files:
            storage_file = next((x for x in self.file_manager.get_files() if x.id == f.id), None)
            if storage_file:
                item = QListWidgetItem(storage_file.filename)
                item.setData(Qt.UserRole, storage_file)
                self.vector_store_display.addItem(item)

    def attach_file(self, item: QListWidgetItem):
        self.set_buttons_state(False, "attaching...")
        file: FileObject = item.data(Qt.UserRole)
        if self.file_manager.attach_file(file):
            self._add_item_to_vector_store(file, item)
        else:
            print(f"Failed to attach file: {file.id}")
        self.set_buttons_state(True)

    def detach_file(self, item: QListWidgetItem):
        print("Detaching file")
        self.set_buttons_state(False, "detaching...")
        file: FileObject = item.data(Qt.UserRole)
        if self.file_manager.detach_file(file):
            self._remove_item_from_vector_store(file, item)
        else:
            print(f"Failed to detach file: {file.id}")
        self.set_buttons_state(True)

    def _add_item_to_vector_store(self, file: FileObject, item: QListWidgetItem):
        new_item = QListWidgetItem(file.filename)
        new_item.setData(Qt.UserRole, file)
        self.vector_store_display.addItem(new_item)
        self.parent.storage_manager.storage_display.takeItem(self.parent.storage_manager.storage_display.row(item))
        print(f"Attached file: {file.id}")

    def _remove_item_from_vector_store(self, file: FileObject, item: QListWidgetItem):
        new_item = QListWidgetItem(file.filename)
        new_item.setData(Qt.UserRole, file)
        self.vector_store_display.takeItem(self.vector_store_display.row(item))
        self.parent.storage_manager.storage_display.addItem(new_item)
        print(f"Detached file: {file.id}")

    def set_buttons_state(self, enabled, action=None):
        self.attach_button.setText(action if not enabled else "attach")
        self.detach_button.setText(action if not enabled else "detach")
        self.attach_button.setEnabled(enabled)
        self.detach_button.setEnabled(enabled)

        storage_manager = self.parent.storage_manager
        storage_manager.upload_button.setText(action if not enabled else "upload")
        storage_manager.remove_button.setText(action if not enabled else "remove")
        storage_manager.upload_button.setEnabled(enabled)
        storage_manager.remove_button.setEnabled(enabled)
