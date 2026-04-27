from .base import WebViewer

class WorldMapViewer(WebViewer):
    def __init__(self):
        super().__init__("https://wmap.gghjk.net")