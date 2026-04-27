from .base import WebViewer

class StatusViewer(WebViewer):
    def __init__(self):
        super().__init__("https://status.gghjk.net")