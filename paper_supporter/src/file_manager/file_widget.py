from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog

from paper_supporter.lib.openai.file_manager import FileManager
from concurrent.futures import ThreadPoolExecutor

from .vector_store_manager import VectorStoreManager
from .storage_manager import StorageManager

from paper_supporter.prerude import ASSISTANT_VECTOR_STORE_ID


class FileWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 500)

        self.main_layout = QVBoxLayout(self)

        vector_store_id = ASSISTANT_VECTOR_STORE_ID.get()
        self.file_manager = FileManager(vector_store_id)
        self.storage_manager = StorageManager(self.file_manager, self)
        self.vector_store_manager = VectorStoreManager(self.file_manager, self, vector_store_id)

        self.main_layout.addLayout(self.vector_store_manager.layout)
        self.main_layout.addLayout(self.storage_manager.layout)

        self.executor = ThreadPoolExecutor(max_workers=2)
        self._initialize_display()

    def _initialize_display(self):
        self.vector_store_manager.update_vector_store_display()
        self.storage_manager.update_storage_display()

    def upload_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            if file_path:
                self.executor.submit(self.storage_manager.upload_file, file_path)

    def remove_file(self):
        selected_items = self.storage_manager.storage_display.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            if item:
                self.executor.submit(self.storage_manager.remove_file, item)

    def attach_file(self):
        selected_items = self.storage_manager.storage_display.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            if item:
                self.executor.submit(self.vector_store_manager.attach_file, item)

    def detach_file(self):
        print("detaching")
        selected_items = self.vector_store_manager.vector_store_display.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            if item:
                self.executor.submit(self.vector_store_manager.detach_file, item)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.executor.submit(self.storage_manager.upload_file, file_path)
