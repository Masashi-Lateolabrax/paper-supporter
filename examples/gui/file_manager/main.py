import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, \
    QFileDialog, QApplication, QListWidgetItem
from openai.types import FileObject

from paper_supporter.lib.openai.file_manager import FileManager

from concurrent.futures import ThreadPoolExecutor

from paper_supporter.env import ASSISTANT_VECTOR_STORE_ID


class FileWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        # Vector Store Section
        self.vector_store_label = QLabel("Vector Store", self)
        self.vector_store_label.setAlignment(Qt.AlignCenter)
        self.vector_store_label.setStyleSheet("text-decoration: underline;")
        self.main_layout.addWidget(self.vector_store_label)

        self.vector_store_display = QListWidget(self)
        self.main_layout.addWidget(self.vector_store_display)

        self.attach_button = QPushButton("attach", self)
        self.attach_button.clicked.connect(self.attach_file)
        self.detach_button = QPushButton("detach", self)
        self.attach_detach_layout = QHBoxLayout()
        self.attach_detach_layout.addWidget(self.attach_button)
        self.attach_detach_layout.addWidget(self.detach_button)
        self.main_layout.addLayout(self.attach_detach_layout)
        self.detach_button.clicked.connect(self.detach_file)

        # Space between sections
        self.space_label = QLabel(" ", self)
        self.main_layout.addWidget(self.space_label)

        # Storage Section
        self.storage_label = QLabel("Storage", self)
        self.storage_label.setAlignment(Qt.AlignCenter)
        self.storage_label.setStyleSheet("text-decoration: underline;")
        self.main_layout.addWidget(self.storage_label)

        self.storage_display = QListWidget(self)
        self.storage_display.setAcceptDrops(True)
        self.storage_display.dragEnterEvent = self.dragEnterEvent
        self.storage_display.dropEvent = self.dropEvent
        self.main_layout.addWidget(self.storage_display)

        self.upload_button = QPushButton("upload", self)
        self.upload_button.clicked.connect(self.upload_file)
        self.remove_button = QPushButton("remove", self)
        self.remove_button.clicked.connect(self.remove_file)
        self.upload_remove_layout = QHBoxLayout()
        self.upload_remove_layout.addWidget(self.upload_button)
        self.upload_remove_layout.addWidget(self.remove_button)
        self.main_layout.addLayout(self.upload_remove_layout)

        self.executor = ThreadPoolExecutor(max_workers=2)
        vector_store_id = ASSISTANT_VECTOR_STORE_ID.get()
        if not vector_store_id:
            self.file_manager = FileManager()
        else:
            self.file_manager = FileManager(vector_store_id=vector_store_id)

        self.initialize_display()

    def initialize_display(self):
        self.update_vector_store_display()
        self.update_storage_display()

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

    def update_storage_display(self):
        self.storage_display.clear()
        for file in self.file_manager.get_files():
            if self.vector_store_display.findItems(file.filename, Qt.MatchExactly):
                continue
            item = QListWidgetItem(file.filename)
            item.setData(Qt.UserRole, file)
            self.storage_display.addItem(item)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.executor.submit(self._upload_file_task, file_path)

    def upload_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.executor.submit(self._upload_file_task, file_path)

    def _upload_file_task(self, file_path):
        self.set_buttons_state(False, "uploading")
        with open(file_path, 'rb') as f:
            file: FileObject = self.file_manager.upload_file(f)
            self.update_storage_display()
            print(f"Uploaded file: {file.id}")
        self.set_buttons_state(True)

    def remove_file(self):
        selected_items = self.storage_display.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.executor.submit(self._remove_file_task, item)

    def _remove_file_task(self, item: QListWidgetItem):
        file: FileObject = item.data(Qt.UserRole)
        self.set_buttons_state(False, "removing")
        if self.file_manager.remove_file(file):
            self.storage_display.takeItem(self.storage_display.row(item))
            print(f"Removed file: {file.id}")
        else:
            print(f"Failed to remove file: {file.id}")
        self.set_buttons_state(True)

    def attach_file(self):
        selected_items = self.storage_display.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.executor.submit(self._attach_file_task, item)

    def _attach_file_task(self, item: QListWidgetItem):
        file: FileObject = item.data(Qt.UserRole)
        self.set_buttons_state(False, "attaching")
        if self.file_manager.attach_file(file):
            new_item = QListWidgetItem(file.filename)
            new_item.setData(Qt.UserRole, file)
            self.vector_store_display.addItem(new_item)
            self.storage_display.takeItem(self.storage_display.row(item))
        else:
            print(f"Failed to attach file: {file.id}")
        self.set_buttons_state(True)

    def detach_file(self):
        selected_items = self.vector_store_display.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.executor.submit(self._detach_file_task, item)

    def _detach_file_task(self, item: QListWidgetItem):
        print("detaching")
        file: FileObject = item.data(Qt.UserRole)
        self.set_buttons_state(False, "detaching")
        if self.file_manager.detach_file(file):
            new_item = QListWidgetItem(file.filename)
            new_item.setData(Qt.UserRole, file)
            self.storage_display.addItem(new_item)
            self.vector_store_display.takeItem(self.vector_store_display.row(item))
            print(f"Detached file: {file.id}")
        else:
            print(f"Failed to detach file: {file.id}")
        self.set_buttons_state(True)

    def set_buttons_state(self, enabled, action=None):
        if enabled:
            self.attach_button.setText("attach")
            self.detach_button.setText("detach")
            self.upload_button.setText("upload")
            self.remove_button.setText("remove")
        else:
            self.attach_button.setText(action)
            self.detach_button.setText(action)
            self.upload_button.setText(action)
            self.remove_button.setText(action)

        self.attach_button.setEnabled(enabled)
        self.detach_button.setEnabled(enabled)
        self.upload_button.setEnabled(enabled)
        self.remove_button.setEnabled(enabled)

    def closeEvent(self, event):
        ASSISTANT_VECTOR_STORE_ID.set(self.file_manager.vector_store.id)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileWindow()
    window.show()
    sys.exit(app.exec())
