import pandas as pd
import numpy as np

# Read CSV, skip headers before $$SOE
with open("voyager1.csv", "r") as f:
    lines = f.readlines()

start_idx = 0
for i, line in enumerate(lines):
    if line.startswith("$$SOE"):
        start_idx = i + 1
        break

# Read only data lines
data_lines = lines[start_idx:]
with open("voyager_temp.csv", "w") as f:
    f.writelines(data_lines)

# Column names matching CSV structure
columns = ["Date", "empty1", "empty2", "Azi", "Elev", "Delta", "Deldot", "OneWay_LT"]

# Load CSV
data = pd.read_csv("voyager_temp.csv", names=columns, skip_blank_lines=True)

# Keep only needed columns
VOYAGER_EVENTS = data[["Date", "Azi", "Elev", "Delta"]].copy()

# Convert to numeric
VOYAGER_EVENTS["Azi"] = pd.to_numeric(VOYAGER_EVENTS["Azi"], errors="coerce")
VOYAGER_EVENTS["Elev"] = pd.to_numeric(VOYAGER_EVENTS["Elev"], errors="coerce")
VOYAGER_EVENTS["Delta"] = pd.to_numeric(VOYAGER_EVENTS["Delta"], errors="coerce")

# Drop NaNs
VOYAGER_EVENTS = VOYAGER_EVENTS.dropna().reset_index(drop=True)

# Create simple X,Y,Z for 3D plotting
VOYAGER_EVENTS["X"] = VOYAGER_EVENTS["Delta"] * np.cos(np.radians(VOYAGER_EVENTS["Elev"])) * np.cos(np.radians(VOYAGER_EVENTS["Azi"]))
VOYAGER_EVENTS["Y"] = VOYAGER_EVENTS["Delta"] * np.cos(np.radians(VOYAGER_EVENTS["Elev"])) * np.sin(np.radians(VOYAGER_EVENTS["Azi"]))
VOYAGER_EVENTS["Z"] = VOYAGER_EVENTS["Delta"] * np.sin(np.radians(VOYAGER_EVENTS["Elev"]))
