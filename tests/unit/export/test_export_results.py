# test_compute_distances.py
import os
import tempfile
import pytest
from PIL import Image
from compute_distances import compute_distances, generate_csv_export, generate_png_export

def test_compute_distances():
    points = [(0, 0), (3, 4), (6, 8)]
    result = compute_distances(points)
    assert pytest.approx(result, 0.01) == 10.0

def test_generate_csv_export_creates_file_and_content():
    points = [(1, 2), (3, 4)]
    total_distance = 2.828
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, 'results.csv')
        generate_csv_export(points, total_distance, csv_path)
        assert os.path.exists(csv_path)
        with open(csv_path, 'r') as f:
            lines = f.readlines()
        assert lines[0].strip() == 'X,Y'
        assert lines[1].strip() == '1,2'
        assert lines[2].strip() == '3,4'
        assert lines[3].strip() == 'Total Distance,2.828'

def test_generate_png_export_saves_image():
    img = Image.new('RGB', (100, 100), color='blue')
    points = [(0, 0), (1, 1)]
    with tempfile.TemporaryDirectory() as tmpdir:
        image_path = os.path.join(tmpdir, 'results.png')
        generate_png_export(points, img, image_path)
        assert os.path.exists(image_path)
        loaded_img = Image.open(image_path)
        assert loaded_img.size == (100, 100)