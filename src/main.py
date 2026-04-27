import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt

from webview.element_web import ElementViewer
from webview.system_map import SystemMapViewer
from webview.world_map import WorldMapViewer
from webview.status_web import StatusViewer
from webview.main_web import MainViewer


# ---------------- HOME PAGE ----------------
class HomePage(QWidget):
    def __init__(self, open_tab):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("🏠 GGHJK App")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel("Vyber Aplikaci")
        subtitle.setStyleSheet("color: gray; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        row = QHBoxLayout()

        row.addWidget(self.card("🌐 Element", lambda: open_tab("element")))
        row.addWidget(self.card("🗺 System Map", lambda: open_tab("system")))
        row.addWidget(self.card("🌍 World Map", lambda: open_tab("world")))
        row.addWidget(self.card("📊 Status", lambda: open_tab("status")))
        row.addWidget(self.card("📩 Tickety", lambda: open_tab("main")))


        layout.addLayout(row)

        self.setLayout(layout)

    def card(self, title, action):
        frame = QFrame()
        frame.setFixedSize(220, 120)

        frame.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-radius: 12px;
            }
            QFrame:hover {
                background-color: #3a3a3a;
            }
        """)

        layout = QVBoxLayout()

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white; font-size: 14px;")

        btn = QPushButton("Open")
        btn.clicked.connect(action)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #5c5cff;
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #7878ff;
            }
        """)

        layout.addWidget(label)
        layout.addWidget(btn)

        frame.setLayout(layout)
        return frame


# ---------------- MAIN APP ----------------
class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Maps")
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.setCentralWidget(self.tabs)

        # HOME TAB
        self.add_home()

    # ---------------- HOME ----------------
    def add_home(self):
        self.home = HomePage(self.open_tab)
        self.tabs.addTab(self.home, "Home")

    # ---------------- CLOSE TAB FIX ----------------
    def close_tab(self, index):
        self.tabs.removeTab(index)

    # ---------------- OPEN TABS ----------------
    def open_tab(self, name):

        # 🔥 vždy nová instance (FIX element bug)
        if name == "element":
            widget = ElementViewer()
            title = "Element"

        elif name == "system":
            widget = SystemMapViewer()
            title = "MTR System Map"

        elif name == "world":
            widget = WorldMapViewer()
            title = "World Map"

        elif name == "status":
            widget = StatusViewer()
            title = "Status"

        elif name == "main":
            widget = MainViewer()
            title = "Tickety"

        else:
            return

        self.tabs.addTab(widget, title)
        self.tabs.setCurrentWidget(widget)


# ---------------- RUN ----------------
app = QApplication(sys.argv)

window = App()
window.show()

sys.exit(app.exec())