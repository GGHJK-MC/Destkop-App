from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class WebViewer(QWebEngineView):
    def __init__(self, url: str):
        super().__init__()
        self.setWindowTitle(url)
        self.resize(1024, 768)
        self.load(QUrl(url))