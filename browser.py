from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WebViewer")
        self.setGeometry(100, 100, 1200, 800)

        # widgets
        self.input = QLineEdit()
        self.input.setPlaceholderText("type a page name......")

        self.btn = QPushButton("Go")
        self.btn.clicked.connect(self.load)

        self.view = QWebEngineView()
        self.view.setUrl(QUrl("http://127.0.0.1:8085/"))

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.btn)
        layout.addWidget(self.view)

        main = QWidget()
        main.setLayout(layout)
        self.setCentralWidget(main)

    def loader(self):
        text = self.input.text().strip()
        if text:
            if ".html" not in text:
                text = text + ".html"
            url = f"http://127.0.0.1:8085/{text}"
            self.view.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Browser()
    win.show()
    sys.exit(app.exec_())

