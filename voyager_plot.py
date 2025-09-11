import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_voyager(events, highlighted=None, view="3d", max_points=15):
    """
    Plot Voyager path in dark mode.
    Shows only `max_points` points for clarity,
    but allows highlighting/searching any real data.
    """

    # Limit number of displayed points
    display_events = events[-max_points:] if len(events) > max_points else events

    x = [e["coords"][0] for e in display_events]
    y = [e["coords"][1] for e in display_events]
    z = [e["coords"][2] for e in display_events]
    labels = [f"{e['year']}: {e['event']}" for e in display_events]

    # Dark mode style
    plt.style.use("dark_background")

    if view == "3d":
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection="3d")
        ax.plot(x, y, z, color="#00bcd4", marker="o", markersize=6, label="Voyager Path")

        # Highlighted point
        if highlighted:
            hx, hy, hz = highlighted["coords"]
            ax.scatter(hx, hy, hz, color="#ff9800", s=100, label=f"Selected: {highlighted['year']}")
            ax.text(hx, hy, hz, f"{highlighted['year']} - {highlighted['event']}", color="#ff9800")

        ax.set_title("🚀 Voyager Trajectory (3D)", color="white", fontsize=14)
        ax.set_xlabel("X (km)", color="white")
        ax.set_ylabel("Y (km)", color="white")
        ax.set_zlabel("Z (km)", color="white")

    else:  # 2D view
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.plot(x, y, color="#00bcd4", marker="o", markersize=6, label="Voyager Path")

        for i, label in enumerate(labels):
            ax.text(x[i], y[i], label, fontsize=8, color="lightgray")

        # Highlighted point
        if highlighted:
            hx, hy, _ = highlighted["coords"]
            ax.scatter(hx, hy, color="#ff9800", s=100, label=f"Selected: {highlighted['year']}")
            ax.text(hx, hy, f"{highlighted['year']} - {highlighted['event']}", color="#ff9800")

        ax.set_title("🚀 Voyager Trajectory (2D)", color="white", fontsize=14)
        ax.set_xlabel("X (km)", color="white")
        ax.set_ylabel("Y (km)", color="white")

    ax.legend()
    plt.show()
