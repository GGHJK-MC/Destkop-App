from .base import WebViewer

class ElementViewer(WebViewer):
    def __init__(self):
        super().__init__("https://app.element.io/#/login?hs_url=https://ecmp.gghjk.net")