import matplotlib.pyplot as ppl
import os
from typing import List, Tuple
from io import BytesIO
from matplotlib.figure import Figure

MARGIN_RATE = 0.05
OUTPUT_FOLDER = "results"

Point = Tuple[float, float]

# Example points: [(x, y), ...]
points_data = [
    (2.0, 3.0),
    (5.0, 7.0),
    (9.0, 6.0),
    (12.0, 2.0),
]

def compute_bounds(xs: List[float], ys: List[float], margin_rate: float) -> Tuple[float, float, float, float]:
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    x_margin = margin_rate * (x_max - x_min)
    y_margin = margin_rate * (y_max - y_min)

    return (x_min - x_margin, x_max + x_margin,
            y_min - y_margin, y_max + y_margin)

def plot_points_and_arrows(points: List[Point]):
    for i, (x, y) in enumerate(points):
        ppl.plot(x, y, 'o', markersize=8)
        ppl.text(x + 0.2, y + 0.2, str(i + 1), fontsize=9)
        
        # Draw arrow to next point if not the last point
        if i < len(points) - 1:
            next_x, next_y = points[i + 1]
            ppl.arrow(x, y, next_x - x, next_y - y,
                      length_includes_head=True,
                      head_width=0.3, head_length=0.4,
                      fc='red', ec='red')

def get_png_bytes(fig: Figure) -> bytes:
    """Convert matplotlib figure to PNG bytes."""
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf.getvalue()

def draw_map(points: List[Point], x_min: float = -10.0, x_max: float = 10.0, 
           y_min: float = -10.0, y_max: float = 10.0) -> Figure:
    """Draw the map with points and arrows."""
    fig = ppl.figure(figsize=(8, 6))
    ppl.xlim(x_min, x_max)
    ppl.ylim(y_min, y_max)

    plot_points_and_arrows(points)

    ppl.title("Solved TSP results map")
    ppl.xlabel("X")
    ppl.ylabel("Y")
    ppl.grid(True)
    
    return fig

def generate_png_export(points: List[Point]) -> bytes:
    """Generate a PNG image of the map and return it as bytes.
    
    Args:
        points: List of (x, y) coordinates to plot.
        
    Returns:
        bytes: PNG image data.
        
    Raises:
        ValueError: If points list is empty.
    """
    if not points:
        raise ValueError("Points list cannot be empty")
        
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    x_min, x_max, y_min, y_max = compute_bounds(xs, ys, MARGIN_RATE)

    fig = draw_map(points, x_min, x_max, y_min, y_max)
    png_data = get_png_bytes(fig)
    ppl.close(fig)  # Clean up matplotlib figure
    
    return png_data

def save_map(png_data: bytes, filename: str) -> None:
    """Save PNG data to a file."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    with open(filepath, 'wb') as f:
        f.write(png_data)
    print(f"Map saved to {filepath}")

# Example usage
if __name__ == "__main__":
    png_data = generate_png_export(points_data)
    save_map(png_data, "map.png")
