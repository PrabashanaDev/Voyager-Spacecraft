# main.py
import sys
from PyQt5.QtWidgets import QApplication
from voyager_ui import MainWindow

def load_stylesheet(app):
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠ style.qss not found, running with default theme.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)  # Apply modern theme
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
