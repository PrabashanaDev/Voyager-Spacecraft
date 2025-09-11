# voyager_ui.py
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import QTimer
from voyager_plot import VoyagerPlot
from voyager_data import VOYAGER_EVENTS


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 Voyager 1 Interactive Path Viewer")
        self.setMinimumSize(1000, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        # Left: 3D Plot
        self.plot_widget = VoyagerPlot(self)
        layout.addWidget(self.plot_widget, 2)

        # Right: Event List + Details
        right_panel = QVBoxLayout()

        title_label = QLabel("🛰️ Voyager 1 Mission Events")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3c82f6;")

        self.event_list = QListWidget()
        for e in VOYAGER_EVENTS:
            self.event_list.addItem(f"{e['year']} - {e['event']}")

        self.details_label = QLabel("Voyager is moving...\nEvents update automatically.")
        self.details_label.setWordWrap(True)
        self.details_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.details_label.setStyleSheet("padding: 8px; background: #2b2b3c; border-radius: 6px;")

        # Buttons for control
        self.start_btn = QPushButton("▶ Start")
        self.stop_btn = QPushButton("⏸ Pause")
        self.reset_btn = QPushButton("⏮ Reset")

        self.start_btn.clicked.connect(self.start_animation)
        self.stop_btn.clicked.connect(self.stop_animation)
        self.reset_btn.clicked.connect(self.reset_animation)

        # Add widgets
        right_panel.addWidget(title_label)
        right_panel.addWidget(self.event_list)
        right_panel.addWidget(QLabel("📌 Details:"))
        right_panel.addWidget(self.details_label)
        right_panel.addWidget(self.start_btn)
        right_panel.addWidget(self.stop_btn)
        right_panel.addWidget(self.reset_btn)
        right_panel.addStretch()

        layout.addLayout(right_panel, 1)

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_voyager)
        self.timer.start(200)  # update every 200 ms

    # === Controls ===
    def start_animation(self):
        self.timer.start(200)

    def stop_animation(self):
        self.timer.stop()

    def reset_animation(self):
        self.plot_widget.current_index = 0
        self.plot_widget.plot_trajectory()

    def animate_voyager(self):
        self.plot_widget.move_forward()
        x, y, z = self.plot_widget.get_current_position()

        # Check if near an event
        for e in VOYAGER_EVENTS:
            ex, ey, ez = e["coords"]
            dist = np.sqrt((x - ex) ** 2 + (y - ey) ** 2 + (z - ez) ** 2)
            if dist < 1e9:  # within "close" range
                self.details_label.setText(
                    f"Year: {e['year']}\n"
                    f"Event: {e['event']}\n"
                    f"Position: ({x:.2e}, {y:.2e}, {z:.2e}) km"
                )
                return

        # Otherwise show current position only
        self.details_label.setText(
            f"Voyager position:\n({x:.2e}, {y:.2e}, {z:.2e}) km"
        )
