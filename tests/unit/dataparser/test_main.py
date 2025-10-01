import pytest
from src.dataparser.main import load_tsp_data

def test_load_tsp_data_invalid_extension():
    path = "data/dataset.csv"
    with pytest.raises(ValueError, match="File must be a .tsp file"):
        load_tsp_data(path)

def test_load_tsp_data_inexistent_file():
    path = "data/TSPLIB/a2801312321312.tsp"
    with pytest.raises(ValueError, match="does not exist"):
        load_tsp_data(path)

def test_load_tsp_data_empty_file(tmp_path):
    path = tmp_path / "empty.tsp"
    path.write_text("\n")
    with pytest.raises(TypeError, match="Could not retrieve a list of \\(x, y\\) coordinates"):
        load_tsp_data(str(path))

def test_load_tsp_data_no_eof(tmp_path):
    content = (
        "NAME: sample\n"
        "TYPE: TSP\n"
        "NODE_COORD_SECTION\n"
        "1 10 20\n"
        "2 30 40\n"
        "3 50 60\n"
        "\n"
    )
    path = tmp_path / "no_eof.tsp"
    path.write_text(content)
    result = load_tsp_data(str(path))
    assert result == [("10", "20"), ("30", "40"), ("50", "60")]

def test_load_tsp_data_valid_file(tmp_path):
    content = (
        "NAME: sample\n"
        "TYPE: TSP\n"
        "NODE_COORD_SECTION\n"
        "1 10 20\n"
        "2 30 40\n"
        "3 50 60\n"
        "EOF\n"
    )
    path = tmp_path / "valid.tsp"
    path.write_text(content)
    result = load_tsp_data(str(path))
    assert result == [("10", "20"), ("30", "40"), ("50", "60")]

def test_load_tsp_data_no_node_section(tmp_path):
    content = (
        "NAME: sample\n"
        "TYPE: TSP\n"
        "EOF\n"
    )
    path = tmp_path / "no_node_section.tsp"
    path.write_text(content)
    with pytest.raises(TypeError, match="Could not retrieve a list of \\(x, y\\) coordinates"):
        load_tsp_data(str(path))

def test_load_tsp_data_irregular_spacing(tmp_path):
    content = (
        "NAME: sample\n"
        "TYPE: TSP\n"
        "NODE_COORD_SECTION\n"
        "1    10    20\n"
        "2  30     40\n"
        "3      50 60\n"
        "EOF\n"
    )
    path = tmp_path / "irregular_spacing.tsp"
    path.write_text(content)
    result = load_tsp_data(str(path))
    assert result == [("10", "20"), ("30", "40"), ("50", "60")]