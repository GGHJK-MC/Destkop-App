from .base import WebViewer

class SystemMapViewer(WebViewer):
    def __init__(self):
        super().__init__("https://smap.gghjk.net/index.html")