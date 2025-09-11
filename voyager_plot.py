import numpy as np
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from voyager_data import VOYAGER_EVENTS

class VoyagerPlot2D(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(6, 6))
        super().__init__(fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)
        self.current_index = 0
        self.trail_length = 50  # last N points for trail
        self.plot_trajectory()

    def plot_trajectory(self):
        self.axes.clear()
        # Plot trail
        start = max(0, self.current_index - self.trail_length)
        self.axes.plot(
            VOYAGER_EVENTS["Azi"].iloc[start:self.current_index+1],
            VOYAGER_EVENTS["Elev"].iloc[start:self.current_index+1],
            "b-", alpha=0.7
        )
        # Current position
        self.axes.scatter(
            VOYAGER_EVENTS["Azi"].iloc[self.current_index],
            VOYAGER_EVENTS["Elev"].iloc[self.current_index],
            s=100, color="red", label="Voyager"
        )
        self.axes.set_xlabel("Azimuth (deg)")
        self.axes.set_ylabel("Elevation (deg)")
        self.axes.set_title("Voyager 2D Top-Down View")
        self.axes.legend()
        self.draw()

    def move_forward(self):
        self.current_index = (self.current_index + 1) % len(VOYAGER_EVENTS)
        self.plot_trajectory()

    def get_current_position(self):
        return (
            VOYAGER_EVENTS["Date"].iloc[self.current_index],
            VOYAGER_EVENTS["Delta"].iloc[self.current_index]
        )


class VoyagerPlot3D(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(6, 6))
        super().__init__(fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111, projection="3d")
        self.current_index = 0
        self.num_steps = len(VOYAGER_EVENTS)
        self.plot_trajectory()

    def plot_trajectory(self):
        self.axes.clear()
        # Plot trajectory
        self.axes.plot(
            VOYAGER_EVENTS["X"],
            VOYAGER_EVENTS["Y"],
            VOYAGER_EVENTS["Z"],
            "r--", label="Voyager Path"
        )
        # Current position
        cx = VOYAGER_EVENTS["X"].iloc[self.current_index]
        cy = VOYAGER_EVENTS["Y"].iloc[self.current_index]
        cz = VOYAGER_EVENTS["Z"].iloc[self.current_index]
        self.axes.scatter(cx, cy, cz, s=100, color="gold", marker="*", label="Voyager")
        self.axes.set_xlabel("X (km)")
        self.axes.set_ylabel("Y (km)")
        self.axes.set_zlabel("Z (km)")
        self.axes.set_title("Voyager 3D Path")
        self.axes.legend()
        self.draw()

    def move_forward(self):
        self.current_index = (self.current_index + 1) % self.num_steps
        self.plot_trajectory()

    def get_current_position(self):
        return (
            VOYAGER_EVENTS["Date"].iloc[self.current_index],
            VOYAGER_EVENTS["Delta"].iloc[self.current_index]
        )
