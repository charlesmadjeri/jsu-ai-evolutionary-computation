import matplotlib.pyplot as ppl
import numpy as np
import os

MARGIN_RATE = 0.05
OUTPUT_FOLDER = "results"

# Example data: [id, x, y, next_id]
data = [
    [1, 2, 3, 3],
    [2, 5, 7, 4],
    [3, 9, 6, 2],
    [4, 12, 2, None],
]

def build_points(data):
    return {row[0]: (row[1], row[2], row[3]) for row in data}

def compute_bounds(xs, ys, margin_rate):
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    x_margin = margin_rate * (x_max - x_min)
    y_margin = margin_rate * (y_max - y_min)

    return (x_min - x_margin, x_max + x_margin,
            y_min - y_margin, y_max + y_margin)

def plot_points_and_arrows(points):
    for pid, (x, y, next_id) in points.items():
        ppl.plot(x, y, 'o', markersize=8)
        ppl.text(x + 0.2, y + 0.2, str(pid), fontsize=9)

        if next_id in points:
            nx, ny, _ = points[next_id]
            ppl.arrow(x, y, nx - x, ny - y,
                      length_includes_head=True,
                      head_width=0.3, head_length=0.4,
                      fc='red', ec='red')

def save_map(filename):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    ppl.savefig(filepath)
    print(f"Map saved to {filepath}")

def draw_map(data, save_filename=None):
    points = build_points(data)
    xs = [row[1] for row in data]
    ys = [row[2] for row in data]

    x_min, x_max, y_min, y_max = compute_bounds(xs, ys, MARGIN_RATE)

    ppl.figure(figsize=(8, 6))
    ppl.xlim(x_min, x_max)
    ppl.ylim(y_min, y_max)

    plot_points_and_arrows(points)

    ppl.title("Solved TSP Map")
    ppl.xlabel("X axis")
    ppl.ylabel("Y axis")
    ppl.grid(True)

    if save_filename:
        save_map(save_filename)
    else:
        ppl.show()

# Run
if __name__ == "__main__":
    draw_map(data, save_filename="map.png")
