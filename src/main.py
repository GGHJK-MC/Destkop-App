import sys
import os
import requests
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

try:
    from webview.element_web import ElementViewer
    from webview.system_map import SystemMapViewer
    from webview.world_map import WorldMapViewer
    from webview.status_web import StatusViewer
    from webview.main_web import MainViewer
except ImportError as e:
    print(f"Chyba importu webview modulů: {e}")

CURRENT_VERSION = "1.2.0"
VERSION_URL = "https://raw.githubusercontent.com/GGHJK-MC/Destkop-App/refs/heads/master/verisons/new.json"
INSTALLER_URL = "https://github.com/GGHJK-MC/Destkop-App/releases/download/1.0.0/GGHJK_Installer"

class InstallWorker(QThread):
    finished = pyqtSignal(bool, str, str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            temp_dir = os.path.join(os.path.expanduser("~"), ".gghjk_temp")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            installer_path = os.path.join(temp_dir, "GGHJK_Installer")

            response = requests.get(self.url, timeout=30)
            if response.status_code == 200:
                with open(installer_path, 'wb') as f:
                    f.write(response.content)

                self.finished.emit(True, "Instalátor stažen. Aplikace se nyní restartuje pro aktualizaci.", installer_path)
            else:
                self.finished.emit(False, f"Chyba serveru: {response.status_code}", "")
        except Exception as e:
            self.finished.emit(False, str(e), "")

class UpdateChecker(QThread):
    update_available = pyqtSignal(str, str, str)

    def run(self):
        try:
            response = requests.get(VERSION_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    latest = data[0]
                    if latest.get("version") != CURRENT_VERSION:
                        self.update_available.emit(
                            latest.get("version"),
                            latest.get("description"),
                            INSTALLER_URL
                        )
        except:
            pass

class HomePage(QWidget):
    def __init__(self, open_tab):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("🏠 GGHJK App")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel(f"Vyber Aplikaci | v{CURRENT_VERSION}")
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
        frame.setStyleSheet("QFrame { background-color: #2b2b2b; border-radius: 12px; } QFrame:hover { background-color: #3a3a3a; }")
        l = QVBoxLayout()
        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white; font-size: 14px;")
        btn = QPushButton("Open")
        btn.clicked.connect(action)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("QPushButton { background-color: #5c5cff; color: white; border-radius: 6px; padding: 6px; } QPushButton:hover { background-color: #7878ff; }")
        l.addWidget(label)
        l.addWidget(btn)
        frame.setLayout(l)
        return frame

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GGHJK Desktop")
        self.resize(1200, 800)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        self.add_home()

        self.updater = UpdateChecker()
        self.updater.update_available.connect(self.show_update_dialog)
        self.updater.start()

    def add_home(self):
        self.home = HomePage(self.open_tab)
        self.tabs.addTab(self.home, "Home")

    def close_tab(self, index):
        if index != 0: self.tabs.removeTab(index)

    def show_update_dialog(self, version, desc, url):
        if QMessageBox.question(self, "Aktualizace", f"Nová verze {version} je k dispozici.\n\n{desc}\n\nStáhnout?") == QMessageBox.StandardButton.Yes:
            self.installer_worker = InstallWorker(url)
            self.installer_worker.finished.connect(self.finalize_update)
            self.installer_worker.start()

    def finalize_update(self, success, message, installer_path):
        if not success:
            QMessageBox.warning(self, "Chyba", message)
            return

        os.chmod(installer_path, 0o755)
        subprocess.Popen([installer_path])
        sys.exit()

    def open_tab(self, name):
        mapping = {
            "element": (ElementViewer, "Element"),
            "system": (SystemMapViewer, "MTR System Map"),
            "world": (WorldMapViewer, "World Map"),
            "status": (StatusViewer, "Status"),
            "main": (MainViewer, "Tickety")
        }
        if name in mapping:
            cls, title = mapping[name]
            widget = cls()
            index = self.tabs.addTab(widget, title)
            self.tabs.setCurrentIndex(index)

if __name__ == "__main__":
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = App()
    window.show()
    sys.exit(app.exec())