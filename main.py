import tkinter as tk
from tkinter import ttk, messagebox
from voyager_data import VOYAGER_EVENTS
from voyager_plot import plot_voyager

# === Dark Theme Colors ===
BG_COLOR = "#121212"
FG_COLOR = "#e0e0e0"
ACCENT_COLOR = "#00bcd4"
HIGHLIGHT_COLOR = "#ff9800"

def search_event():
    year = year_entry.get()
    if not year.isdigit():
        messagebox.showwarning("Warning", "Please enter a valid year.")
        return

    year = int(year)
    for event in VOYAGER_EVENTS:
        if event["year"] == year:
            messagebox.showinfo("Voyager Event Found",
                                f"Year: {event['year']}\nEvent: {event['event']}\nCoords: {event['coords']}")
            return
    messagebox.showerror("Not Found", f"No data found for {year}.")

def plot_view(view="3d"):
    year = year_entry.get()
    highlighted = None
    if year.isdigit():
        year = int(year)
        highlighted = next((e for e in VOYAGER_EVENTS if e["year"] == year), None)
    plot_voyager(VOYAGER_EVENTS, highlighted=highlighted, view=view)

# === UI Setup ===
root = tk.Tk()
root.title("🚀 Voyager Spacecraft Tracker")
root.configure(bg=BG_COLOR)

# Title
title_label = tk.Label(root, text="Voyager Spacecraft Tracker",
                       font=("Arial", 16, "bold"),
                       fg=ACCENT_COLOR, bg=BG_COLOR)
title_label.pack(pady=10)

# Search
frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(pady=10)

tk.Label(frame, text="Enter Year:",
         fg=FG_COLOR, bg=BG_COLOR,
         font=("Arial", 12)).grid(row=0, column=0, padx=5)

year_entry = tk.Entry(frame, font=("Arial", 12),
                      bg="#1e1e1e", fg=FG_COLOR,
                      insertbackground=FG_COLOR)
year_entry.grid(row=0, column=1, padx=5)

search_button = tk.Button(frame, text="🔍 Search",
                          command=search_event,
                          bg=ACCENT_COLOR, fg="black",
                          font=("Arial", 12, "bold"))
search_button.grid(row=0, column=2, padx=5)

# Plot buttons
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

btn_2d = tk.Button(btn_frame, text="📉 Show 2D Plot",
                   command=lambda: plot_view("2d"),
                   bg="#333333", fg=FG_COLOR,
                   font=("Arial", 12, "bold"))
btn_2d.grid(row=0, column=0, padx=10)

btn_3d = tk.Button(btn_frame, text="🌌 Show 3D Plot",
                   command=lambda: plot_view("3d"),
                   bg="#333333", fg=FG_COLOR,
                   font=("Arial", 12, "bold"))
btn_3d.grid(row=0, column=1, padx=10)

# Data list
tree_frame = tk.Frame(root, bg=BG_COLOR)
tree_frame.pack(pady=10, fill="both", expand=True)

columns = ("Year", "Event", "Coordinates")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

# Style Treeview for dark mode
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#1e1e1e",
                foreground=FG_COLOR,
                fieldbackground="#1e1e1e",
                rowheight=25,
                font=("Arial", 10))
style.configure("Treeview.Heading",
                background=ACCENT_COLOR,
                foreground="black",
                font=("Arial", 11, "bold"))
style.map("Treeview",
          background=[("selected", HIGHLIGHT_COLOR)],
          foreground=[("selected", "black")])

tree.pack(fill="both", expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

for event in VOYAGER_EVENTS:
    tree.insert("", "end", values=(event["year"], event["event"], event["coords"]))

root.mainloop()
