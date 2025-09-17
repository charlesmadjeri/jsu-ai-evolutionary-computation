import pytest
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
from src.export.generate_png_export import (
    compute_bounds,
    draw_map,
    get_png_bytes,
    generate_png_export,
)

# Test data
SAMPLE_POINTS = [
    (2.0, 3.0),  # Point 1
    (5.0, 7.0),  # Point 2
    (9.0, 6.0),  # Point 3
    (12.0, 2.0), # Point 4
]

def test_compute_bounds():
    """Test the compute_bounds function with known values."""
    xs = [p[0] for p in SAMPLE_POINTS]
    ys = [p[1] for p in SAMPLE_POINTS]
    margin_rate = 0.05
    
    x_min, x_max, y_min, y_max = compute_bounds(xs, ys, margin_rate)
    
    # Calculate expected values
    expected_x_margin = (12.0 - 2.0) * margin_rate
    expected_y_margin = (7.0 - 2.0) * margin_rate
    
    assert x_min == pytest.approx(2.0 - expected_x_margin)
    assert x_max == pytest.approx(12.0 + expected_x_margin)
    assert y_min == pytest.approx(2.0 - expected_y_margin)
    assert y_max == pytest.approx(7.0 + expected_y_margin)

def test_draw_map():
    """Test that draw_map creates a valid matplotlib figure."""
    fig = draw_map(SAMPLE_POINTS)
    
    assert isinstance(fig, plt.Figure)
    assert len(fig.axes) == 1  # Should have one subplot
    
    ax = fig.axes[0]
    assert ax.get_title() == "Solved TSP results map"
    assert ax.get_xlabel() == "X"
    assert ax.get_ylabel() == "Y"
    
    plt.close(fig)  # Cleanup

def test_get_png_bytes():
    """Test that get_png_bytes produces valid PNG data."""
    fig = plt.figure()
    plt.plot([1, 2, 3], [1, 2, 3])
    
    png_data = get_png_bytes(fig)
    plt.close(fig)
    
    assert isinstance(png_data, bytes)
    assert len(png_data) > 0
    
    # Verify it's a valid PNG
    img = Image.open(BytesIO(png_data))
    assert img.format == "PNG"
    assert img.size[0] > 0 and img.size[1] > 0

def test_generate_png_export():
    """Test the full PNG export pipeline."""
    png_data = generate_png_export(SAMPLE_POINTS)
    
    # Verify the output is bytes and non-empty
    assert isinstance(png_data, bytes)
    assert len(png_data) > 0
    
    # Verify it's a valid PNG image
    img = Image.open(BytesIO(png_data))
    assert img.format == "PNG"
    assert img.size[0] > 0 and img.size[1] > 0

def test_generate_png_export_empty_points():
    """Test handling of empty points list."""
    with pytest.raises(ValueError):
        generate_png_export([])

def test_generate_png_export_single_point():
    """Test with a single point."""
    single_point = [(5.0, 5.0)]
    png_data = generate_png_export(single_point)
    
    assert isinstance(png_data, bytes)
    assert len(png_data) > 0
    
    img = Image.open(BytesIO(png_data))
    assert img.format == "PNG"
