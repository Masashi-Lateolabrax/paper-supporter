import sys

from PySide6.QtWidgets import QApplication

from .lib.utils import EnvVariable
from .src.app import MainWindow


def main(env_file_path: str):
    env_variable = EnvVariable(env_file_path)
    app = QApplication(sys.argv)
    window = MainWindow(env_variable)
    window.show()
    sys.exit(app.exec())
