import sys, json, time, psutil, sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QProgressBar
from PyQt6.QtCore import QProcess, pyqtSignal, QObject, QTimer

class BlinkTracker(QObject):
    blink_updated = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.parse_output)
        self.process.start("python3", ["eye_blink_counter.py"])
        self.count = 0
    
    def parse_output(self):
        data = self.process.readAllStandardOutput().data().decode()
        for line in data.strip().split('\n'):
            if line.strip():
                try:
                    blink = json.loads(line)['blink_count']
                    if blink > self.count:
                        self.count = blink
                        self.blink_updated.emit(blink)
                except: pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wellness at Work - Eye Tracker")
        self.resize(400, 300)
        
        # FIXED Dark Theme
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #1e1e1e; 
                color: #ffffff; 
            }
            QLabel { 
                color: #ffffff; 
                font-size: 14px;
                padding: 10px;
            }
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
        """)
        
        central = QWidget()
        layout = QVBoxLayout()
        
        self.blink_label = QLabel("🧠 Blinks: 0")
        self.cpu_label = QLabel("💻 CPU: 0%")
        self.mem_label = QLabel("🧮 Memory: 0%")
        self.cpu_bar = QProgressBar()
        self.mem_bar = QProgressBar()
        
        layout.addWidget(self.blink_label)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)
        layout.addWidget(self.mem_label)
        layout.addWidget(self.mem_bar)
        
        central.setLayout(layout)
        self.setCentralWidget(central)
        
        self.tracker = BlinkTracker()
        self.tracker.blink_updated.connect(self.update_blink)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system)
        self.timer.start(1000)
    
    def update_blink(self, count):
        self.blink_label.setText(f"🧠 Blinks: {count}")
    
    def update_system(self):
        cpu = int(psutil.cpu_percent())
        mem = int(psutil.virtual_memory().percent)
        self.cpu_label.setText(f"💻 CPU: {cpu}%")
        self.mem_label.setText(f"🧮 Memory: {mem}%")
        self.cpu_bar.setValue(cpu)
        self.mem_bar.setValue(mem)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
