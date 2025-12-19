import sys
import json
import time
import sqlite3
import subprocess
import threading

import psutil
import requests
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QProgressBar,
    QDialog,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QMessageBox,
)
from PyQt6.QtCore import pyqtSignal, QObject, QTimer


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Wellness at Work")
        self.setModal(True)
        self.user_id = None

        layout = QFormLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("you@example.com")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your name (optional)")

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)

        layout.addRow("Email:", self.email_input)
        layout.addRow("Name:", self.name_input)
        layout.addRow(login_button)

        self.setLayout(layout)

    def handle_login(self):
        email = self.email_input.text().strip()
        if not email or "@" not in email:
            QMessageBox.warning(self, "Invalid email", "Please enter a valid email address.")
            return
        self.user_id = email
        self.accept()


class BlinkTracker(QObject):
    blink_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.count = 0
        self.process = None
        self.start_tracker()

    def start_tracker(self):
        def run_tracker():
            self.process = subprocess.Popen(
                ["python3", "eye_blink_counter.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1,
            )
            while True:
                line = self.process.stdout.readline()
                if not line:
                    break
                try:
                    data = json.loads(line.strip())
                    if data.get("blink_count", 0) > self.count:
                        self.count = data["blink_count"]
                        self.blink_updated.emit(self.count)
                except Exception:
                    # Ignore malformed lines
                    pass

        thread = threading.Thread(target=run_tracker, daemon=True)
        thread.start()


class MainWindow(QMainWindow):
    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id

        self.setWindowTitle("Wellness at Work - Eye Tracker")
        self.resize(450, 350)

        self.setStyleSheet(
            """
            QMainWindow { background-color: #1e1e1e; color: #ffffff; }
            QLabel { color: #ffffff; font-size: 14px; padding: 10px; }
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 5px;
                text-align: center;
                background-color: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #4a90e2;
                border-radius: 3px;
            }
        """
        )

        central = QWidget()
        layout = QVBoxLayout()

        self.blink_label = QLabel("🧠 Blinks: 0 (Starting tracker...)")
        self.status_label = QLabel(f"Status: Launching eye tracker for {self.user_id}...")
        self.cpu_label = QLabel("💻 CPU: 0%")
        self.mem_label = QLabel("🧮 Memory: 0%")
        self.cpu_bar = QProgressBar()
        self.mem_bar = QProgressBar()

        layout.addWidget(self.blink_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)
        layout.addWidget(self.mem_label)
        layout.addWidget(self.mem_bar)

        central.setLayout(layout)
        self.setCentralWidget(central)

        # SQLite for offline storage
        self.conn = sqlite3.connect("blinks_local.db")
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS blinks
               (user_id TEXT, timestamp REAL, count INTEGER,
                cpu REAL, mem REAL, synced INTEGER DEFAULT 0)"""
        )
        self.conn.commit()

        # Eye tracker
        self.tracker = BlinkTracker()
        self.tracker.blink_updated.connect(self.update_blink)

        # System monitor
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system)
        self.timer.start(1000)

    def update_blink(self, count: int):
        self.blink_label.setText(f"🧠 Blinks: {count}")
        self.status_label.setText("✅ LIVE: Tracking + Cloud Sync")

        # Local SQLite write (offline-first)
        ts = time.time()
        cpu_val = psutil.cpu_percent()
        mem_val = psutil.virtual_memory().percent

        self.conn.execute(
            "INSERT INTO blinks VALUES(?, ?, ?, ?, ?, 0)",
            (self.user_id, ts, count, cpu_val, mem_val),
        )
        self.conn.commit()

        # Cloud sync
        try:
            response = requests.post(
                f"http://localhost:3000/blinks/{self.user_id}",
                json=[
                    {
                        "timestamp": ts,
                        "count": count,
                        "cpu": cpu_val,
                        "memory": mem_val,
                    }
                ],
                headers={"x-api-key": "demo-secret"},
                timeout=2,
            )
            if response.status_code == 201:
                print(f"☁️ Synced blink {count}")
                self.conn.execute(
                    "UPDATE blinks SET synced=1 WHERE user_id=? AND count=?",
                    (self.user_id, count),
                )
                self.conn.commit()
        except Exception as e:
            print(f"❌ Offline / sync failed: {e}")

    def update_system(self):
        cpu = int(psutil.cpu_percent())
        mem = int(psutil.virtual_memory().percent)
        self.cpu_label.setText(f"💻 CPU: {cpu}%")
        self.mem_label.setText(f"🧮 Memory: {mem}%")
        self.cpu_bar.setValue(cpu)
        self.mem_bar.setValue(mem)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Login first
    login = LoginDialog()
    if login.exec() != QDialog.DialogCode.Accepted or not login.user_id:
        sys.exit(0)

    window = MainWindow(user_id=login.user_id)
    window.show()
    sys.exit(app.exec())
