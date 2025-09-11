# voyager_plot.py
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from voyager_data import VOYAGER_EVENTS


class VoyagerPlot(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(6, 6))
        super().__init__(fig)
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
