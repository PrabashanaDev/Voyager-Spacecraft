# main.py
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QLabel, QComboBox, QPushButton
)
from PyQt5.QtCore import QTimer
import sys
import numpy as np
from voyager_plot import VoyagerPlot
from voyager_data import VOYAGER_EVENTS


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voyager 1 Interactive Path Viewer")
        self.setMinimumSize(1000, 600)

        # Load QSS style
        try:
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("style.qss not found. Using default style.")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        # Left: Plot
        self.plot_widget = VoyagerPlot(self, mode="3D")
        layout.addWidget(self.plot_widget, 2)

        # Right: Controls + Event List
        right_panel = QVBoxLayout()

        # --- View mode selector ---
        self.view_selector = QComboBox()
        self.view_selector.addItems(["3D View", "2D View"])
        self.view_selector.currentIndexChanged.connect(self.change_view)

        # --- Event list ---
        self.event_list = QListWidget()
        for e in VOYAGER_EVENTS:
            self.event_list.addItem(f"{e['year']} - {e['event']}")

        # --- Details label ---
        self.details_label = QLabel("Voyager is moving...\nEvents update automatically.")
        self.details_label.setWordWrap(True)

        # --- Buttons ---
        self.start_btn = QPushButton("▶ Start")
        self.stop_btn = QPushButton("⏸ Pause")
        self.reset_btn = QPushButton("⏮ Reset")

        self.start_btn.clicked.connect(self.start_animation)
        self.stop_btn.clicked.connect(self.stop_animation)
        self.reset_btn.clicked.connect(self.reset_animation)

        # Add widgets to right panel
        right_panel.addWidget(QLabel("View Mode:"))
        right_panel.addWidget(self.view_selector)
        right_panel.addWidget(QLabel("Mission Events:"))
        right_panel.addWidget(self.event_list)
        right_panel.addWidget(QLabel("Details:"))
        right_panel.addWidget(self.details_label)
        right_panel.addWidget(self.start_btn)
        right_panel.addWidget(self.stop_btn)
        right_panel.addWidget(self.reset_btn)
        right_panel.addStretch()

        layout.addLayout(right_panel, 1)

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_voyager)
        self.timer.start(200)

    # --- Button actions ---
    def start_animation(self):
        self.timer.start(200)

    def stop_animation(self):
        self.timer.stop()

    def reset_animation(self):
        self.plot_widget.current_index = 0
        self.plot_widget.plot_trajectory()

    # --- View change ---
    def change_view(self):
        mode = "3D" if self.view_selector.currentText() == "3D View" else "2D"
        self.plot_widget.set_mode(mode)

    # --- Animation updates ---
    def animate_voyager(self):
        self.plot_widget.move_forward()
        x, y, z = self.plot_widget.get_current_position()

        # Check if near event
        for e in VOYAGER_EVENTS:
            ex, ey, ez = e["coords"]
            dist = np.sqrt((x - ex) ** 2 + (y - ey) ** 2 + (z - ez) ** 2)
            if dist < 1e9:
                self.details_label.setText(
                    f"Year: {e['year']}\n"
                    f"Event: {e['event']}\n"
                    f"Position: ({x:.2e}, {y:.2e}, {z:.2e}) km"
                )
                return

        # Otherwise show current position
        self.details_label.setText(
            f"Voyager position:\n({x:.2e}, {y:.2e}, {z:.2e}) km"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
