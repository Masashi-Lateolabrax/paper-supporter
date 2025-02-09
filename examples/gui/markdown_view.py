import sys

from PySide6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget
import markdown


class MarkdownViewer(QWidget):
    def __init__(self, markdown_text):
        super().__init__()
        self.setWindowTitle("Markdown Viewer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.set_markdown(markdown_text)

    def set_markdown(self, markdown_text):
        html = markdown.markdown(markdown_text.strip())
        print(html)
        self.text_edit.setHtml(html)


def main():
    markdown_text = """
# Sample Markdown

NOT INCLUDE TAB AT BEGINNING OF SENTENCES!

This is a **bold** text and this is *italic* text.

- Item 1
- Item 2
"""

    app = QApplication(sys.argv)
    viewer = MarkdownViewer(markdown_text)
    viewer.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
