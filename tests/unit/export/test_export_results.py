# test_compute_distances.py
import os
import tempfile
import pytest
from PIL import Image
from export_results import compute_distances, generate_csv_export, generate_png_export

def test_compute_distances():
    points = [(0, 0), (3, 4), (6, 8)]
    result = compute_distances(points)
    assert result == pytest.approx(10.0, rel=1e-3)


def test_generate_csv_export_creates_file_and_content():
    points = [(1, 2), (3, 4)]
    total_distance = 2.828
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, 'results.csv')
        generate_csv_export(points, total_distance, csv_path)
        assert os.path.exists(csv_path)
        with open(csv_path, 'r') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]

        # file layout expected:
        # 0: X,Y
        # 1: 1,2
        # 2: 3,4
        # 3: (empty line)
        # 4: Total Distance,2.828
        assert lines[0].strip() == 'X,Y'
        assert lines[1].strip() == '1,2'
        assert lines[2].strip() == '3,4'
        assert lines[3].strip() == ''
        # verify last row label and numeric value
        last_label, last_value = lines[4].split(',', 1)
        assert last_label == 'Total Distance'
        assert float(last_value) == pytest.approx(total_distance, rel=1e-3)
    

def test_generate_png_export_saves_image():
    img = Image.new('RGB', (100, 100), color='blue')
    points = [(0, 0), (1, 1)]
    with tempfile.TemporaryDirectory() as tmpdir:
        image_path = os.path.join(tmpdir, 'results.png')
        generate_png_export(points, img, image_path)
        assert os.path.exists(image_path)
        loaded_img = Image.open(image_path)
        try:
            assert loaded_img.size == (100, 100)
        finally:
            loaded_img.close()