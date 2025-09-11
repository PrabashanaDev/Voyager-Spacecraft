import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QLabel, QPushButton, QStackedWidget
)
from PyQt5.QtCore import QTimer
from voyager_plot import VoyagerPlot2D, VoyagerPlot3D
from voyager_data import VOYAGER_EVENTS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voyager Tracker")
        self.resize(1000, 600)

        # Central layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Left: Stacked widget for plots
        self.plot_stack = QStackedWidget()
        self.plot2d = VoyagerPlot2D(self)
        self.plot3d = VoyagerPlot3D(self)
        self.plot_stack.addWidget(self.plot2d)
        self.plot_stack.addWidget(self.plot3d)
        main_layout.addWidget(self.plot_stack, 2)

        # Right: Controls and details
        right_panel = QVBoxLayout()

        self.event_list = QListWidget()
        for e in VOYAGER_EVENTS["Date"].head(20):  # show first 20 times
            self.event_list.addItem(str(e))

        self.details_label = QLabel("Voyager moving...\nDetails update automatically.")
        self.details_label.setWordWrap(True)

        # Buttons
        self.btn_2d = QPushButton("Switch to 2D")
        self.btn_3d = QPushButton("Switch to 3D")
        self.btn_2d.clicked.connect(lambda: self.plot_stack.setCurrentWidget(self.plot2d))
        self.btn_3d.clicked.connect(lambda: self.plot_stack.setCurrentWidget(self.plot3d))

        right_panel.addWidget(QLabel("Voyager Events:"))
        right_panel.addWidget(self.event_list)
        right_panel.addWidget(self.btn_2d)
        right_panel.addWidget(self.btn_3d)
        right_panel.addWidget(QLabel("Details:"))
        right_panel.addWidget(self.details_label)
        right_panel.addStretch()
        main_layout.addLayout(right_panel, 1)

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_voyager)
        self.timer.start(100)  # adjust speed

    def animate_voyager(self):
        # Move both plots
        self.plot2d.move_forward()
        self.plot3d.move_forward()
        # Update details for active plot
        current_plot = self.plot_stack.currentWidget()
        date, delta = current_plot.get_current_position()
        self.details_label.setText(f"Date: {date}\nDistance: {delta:.2e} km")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
