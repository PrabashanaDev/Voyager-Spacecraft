import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QLabel
)
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# === Historical Data (Sample) ===
VOYAGER_EVENTS = [
    {"year": 1979, "event": "Jupiter Flyby", "coords": (7.78e8, 0, 0)},
    {"year": 1980, "event": "Saturn Flyby", "coords": (1.43e9, 5e7, 0)},
    {"year": 1990, "event": "Family Portrait", "coords": (6e9, 1e9, 0)},
    {"year": 2012, "event": "Entered Interstellar Space", "coords": (1.8e10, 2e9, 1e9)},
    {"year": 2025, "event": "Current Position", "coords": (2.4e10, 3e9, 1.5e9)},
]


class VoyagerPlot(FigureCanvas):
    def _init_(self, parent=None):
        fig = Figure(figsize=(6, 6))
        super()._init_(fig)
        self.axes = fig.add_subplot(111, projection="3d")
        self.setParent(parent)

        # Path arrays
        self.xs = [e["coords"][0] for e in VOYAGER_EVENTS]
        self.ys = [e["coords"][1] for e in VOYAGER_EVENTS]
        self.zs = [e["coords"][2] for e in VOYAGER_EVENTS]

        # Interpolated path for smooth movement
        self.num_steps = 500
        self.path_x = np.linspace(self.xs[0], self.xs[-1], self.num_steps)
        self.path_y = np.linspace(self.ys[0], self.ys[-1], self.num_steps)
        self.path_z = np.linspace(self.zs[0], self.zs[-1], self.num_steps)

        self.current_index = 0
        self.plot_trajectory()

    def plot_trajectory(self):
        self.axes.clear()

        # Plot trajectory line
        self.axes.plot(self.xs, self.ys, self.zs, "r--", label="Voyager 1 Path")

        # Mark milestone events
        for e in VOYAGER_EVENTS:
            x, y, z = e["coords"]
            self.axes.scatter(x, y, z, s=60, marker="o", color="blue")
            self.axes.text(x, y, z, f"{e['year']}", fontsize=8)

        # Draw Voyager marker at current position
        cx, cy, cz = self.path_x[self.current_index], self.path_y[self.current_index], self.path_z[self.current_index]
        self.axes.scatter(cx, cy, cz, s=100, marker="*", color="gold", label="Voyager 1")

        # Labels
        self.axes.set_title("Voyager 1 Interactive Path")
        self.axes.set_xlabel("X (km)")
        self.axes.set_ylabel("Y (km)")
        self.axes.set_zlabel("Z (km)")
        self.axes.legend()
        self.draw()

    def move_forward(self):
        self.current_index = (self.current_index + 1) % self.num_steps
        self.plot_trajectory()

    def get_current_position(self):
        return (
            self.path_x[self.current_index],
            self.path_y[self.current_index],
            self.path_z[self.current_index],
        )


class MainWindow(QMainWindow):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Voyager 1 Interactive Path Viewer")

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
        self.event_list = QListWidget()
        for e in VOYAGER_EVENTS:
            self.event_list.addItem(f"{e['year']} - {e['event']}")

        self.details_label = QLabel("Voyager is moving...\nEvents update automatically.")
        self.details_label.setWordWrap(True)

        right_panel.addWidget(QLabel("Voyager 1 Mission Events:"))
        right_panel.addWidget(self.event_list)
        right_panel.addWidget(QLabel("Details:"))
        right_panel.addWidget(self.details_label)

        layout.addLayout(right_panel, 1)

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_voyager)
        self.timer.start(200)  # update every 200 ms

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


if __name__ == "_main_":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())