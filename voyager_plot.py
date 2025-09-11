# voyager_plot.py
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from voyager_data import VOYAGER_EVENTS


class VoyagerPlot(FigureCanvas):
    def __init__(self, parent=None, mode="3D"):
        self.mode = mode  # "3D" or "2D"
        fig = Figure(figsize=(7, 7), facecolor="white")
        super().__init__(fig)

        if self.mode == "3D":
            self.ax = fig.add_subplot(111, projection="3d", facecolor="white")
        else:
            self.ax = fig.add_subplot(111, facecolor="#1e1e2e")

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

    def set_mode(self, mode):
        """Switch between 3D and 2D modes"""
        self.mode = mode
        self.figure.clear()
        if self.mode == "3D":
            self.ax = self.figure.add_subplot(111, projection="3d", facecolor="white")
        else:
            self.ax = self.figure.add_subplot(111, facecolor="#1e1e2e")
        self.plot_trajectory()

    def plot_trajectory(self):
        self.ax.clear()

        # Voyager position
        cx, cy, cz = (
            self.path_x[self.current_index],
            self.path_y[self.current_index],
            self.path_z[self.current_index],
        )

        if self.mode == "3D":
            # --- 3D Plot ---
            self.ax.plot(self.xs, self.ys, self.zs, color="blue", linestyle="--", linewidth=2, label="Voyager Path")

            for e in VOYAGER_EVENTS:
                x, y, z = e["coords"]
                self.ax.scatter(x, y, z, s=70, marker="o", color="orange")
                self.ax.text(x, y, z, f"{e['year']}", fontsize=8, color="black")

            self.ax.scatter(cx, cy, cz, s=120, marker="*", color="red", label="Voyager 1")

            self.ax.set_title("Voyager 1 Path (3D)", fontsize=13, pad=15)
            self.ax.set_xlabel("X (km)")
            self.ax.set_ylabel("Y (km)")
            self.ax.set_zlabel("Z (km)")
            self.ax.legend()

        else:
            # --- 2D Plot ---
            self.ax.plot(self.xs, self.ys, color="#3c82f6", linestyle="--", linewidth=2)

            for e in VOYAGER_EVENTS:
                x, y, _ = e["coords"]
                self.ax.scatter(x, y, s=60, color="#ffb703")
                self.ax.text(x, y, f"{e['year']}", fontsize=8, color="white")

            self.ax.scatter(cx, cy, s=120, marker="*", color="#00f5d4")

            self.ax.set_title("Top-Down XY Projection", color="white", fontsize=12, pad=10)
            self.ax.set_xlabel("X (km)", color="white")
            self.ax.set_ylabel("Y (km)", color="white")
            self.ax.tick_params(colors="white")

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
