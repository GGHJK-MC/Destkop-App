import os
import sys
import requests
import zipfile
import shutil
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QPushButton, QLabel, QProgressBar, QWidget, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal

# Konfigurace
APP_NAME = "GGHJK_App"
INSTALL_DIR = os.path.join(os.path.expanduser("~"), "gghjk_app")
ZIP_URL = "https://github.com/GGHJK-MC/Destkop-App/releases/download/1.0.0/Archiv.zip"

class InstallWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def run(self):
        try:
            if not os.path.exists(INSTALL_DIR):
                os.makedirs(INSTALL_DIR)

            zip_path = os.path.join(INSTALL_DIR, "install.zip")

            # 1. Stažení
            self.progress.emit(20)
            response = requests.get(ZIP_URL, stream=True)
            if response.status_code == 200:
                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # 2. Rozbalení
                self.progress.emit(60)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(INSTALL_DIR)

                # 3. Úklid
                os.remove(zip_path)

                # 4. Vytvoření Linux Desktop zástupce
                self.create_linux_shortcut()

                self.progress.emit(100)
                self.finished.emit(True, "Instalace dokončena!")
            else:
                self.finished.emit(False, "Chyba při stahování souboru.")
        except Exception as e:
            self.finished.emit(False, str(e))

    def create_linux_shortcut(self):
        desktop_path = os.path.expanduser("~/.local/share/applications/gghjk_app.desktop")
        exec_path = os.path.join(INSTALL_DIR, "main_app_bin") # Cesta k tvé binárce

        content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=GGHJK App
Exec={exec_path}
Icon={INSTALL_DIR}/icon.png
Terminal=false
Categories=Utility;
"""
        with open(desktop_path, "w") as f:
            f.write(content)
        os.chmod(desktop_path, 0o755)

class InstallerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GGHJK App Installer")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        self.label = QLabel(f"Instalovat GGHJK App do {INSTALL_DIR}?")
        self.btn = QPushButton("Spustit Instalaci")
        self.btn.clicked.connect(self.start_install)
        self.pbar = QProgressBar()

        layout.addWidget(self.label)
        layout.addWidget(self.pbar)
        layout.addWidget(self.btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_install(self):
        self.btn.setEnabled(False)
        self.worker = InstallWorker()
        self.worker.progress.connect(self.pbar.setValue)
        self.worker.finished.connect(self.done)
        self.worker.start()

    def done(self, success, msg):
        if success:
            QMessageBox.information(self, "Hotovo", msg)
            sys.exit()
        else:
            QMessageBox.critical(self, "Chyba", msg)
            self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = InstallerUI()
    ui.show()
    sys.exit(app.exec())