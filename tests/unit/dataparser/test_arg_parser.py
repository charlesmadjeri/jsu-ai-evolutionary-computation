import src.dataparser.arg_parser as arg_parser
from pytest import raises, approx
from argparse import ArgumentTypeError

from os import path, fdopen, remove
from tempfile import mkstemp

def test_range_to_str():
    assert arg_parser.range_to_str(min=0, max=10) == "[0, 10]"
    assert arg_parser.range_to_str(min=None, max=10) == "[-inf, 10]"
    assert arg_parser.range_to_str(min=0, max=None) == "[0, inf]"
    assert arg_parser.range_to_str(min=None, max=None) == "[-inf, inf]"

def test_range_checker():
    # numeric ranges
    assert arg_parser.range_checker(value=5, min=0, max=10) == True
    assert arg_parser.range_checker(value=15, min=0, max=10) == False
    assert arg_parser.range_checker(value=-5, min=0, max=10) == False
    assert arg_parser.range_checker(value=None, min=0, max=10) == False

    # none minimum range
    assert arg_parser.range_checker(value=5, min=None, max=10) == True
    assert arg_parser.range_checker(value=15, min=None, max=10) == False
    assert arg_parser.range_checker(value=-5, min=None, max=10) == True
    assert arg_parser.range_checker(value=None, min=None, max=10) == False

    # none maximum range
    assert arg_parser.range_checker(value=5, min=0, max=None) == True
    assert arg_parser.range_checker(value=15, min=0, max=None) == True
    assert arg_parser.range_checker(value=-5, min=0, max=None) == False
    assert arg_parser.range_checker(value=None, min=0, max=None) == False

    # none minimum and maximum range
    assert arg_parser.range_checker(value=5, min=None, max=None) == True
    assert arg_parser.range_checker(value=15, min=None, max=None) == True
    assert arg_parser.range_checker(value=-5, min=None, max=None) == True
    assert arg_parser.range_checker(value=None, min=None, max=None) == True

def test_int_checker():
    assert arg_parser.int_checker(value="5", min=0, max=10) == 5
    assert arg_parser.int_checker(value=5, min=0, max=10) == 5
    
    # shouldn't parse float
    assert arg_parser.int_checker(value="5.5", min=0, max=10) is None
    assert arg_parser.int_checker(value=5.5, min=0, max=10) is None

    # shouldn't parse string
    assert arg_parser.int_checker(value="abc", min=0, max=10) is None
    assert arg_parser.int_checker(value=None, min=0, max=10) is None

    # shouldn't parse out of range
    raises(ArgumentTypeError, arg_parser.int_checker, value=15, min=0, max=10)
    raises(ArgumentTypeError, arg_parser.int_checker, value=-5, min=0, max=10)

def test_float_checker():
    assert arg_parser.float_checker(value="5.5", min=0, max=10) == approx(5.5)
    assert arg_parser.float_checker(value=5.5, min=0, max=10) == approx(5.5)
    
    # shouldn't parse integer
    assert arg_parser.float_checker(value="5", min=0, max=10) is None
    assert arg_parser.float_checker(value=5, min=0, max=10) is None

    # shouldn't parse string
    assert arg_parser.float_checker(value="abc", min=0, max=10) is None
    assert arg_parser.float_checker(value=None, min=0, max=10) is None


def test_int_or_float_checker():
    # int range shouldn't affect float range
    assert arg_parser.int_or_float_checker(value=5.5, int_min=10, int_max=100, float_min=0, float_max=10) == approx(5.5)
    assert arg_parser.int_or_float_checker(value="5.5", int_min=10, int_max=100, float_min=0, float_max=10) == approx(5.5)
    assert arg_parser.int_or_float_checker(value="5.5", int_min=None, int_max=None, float_min=0, float_max=10) == approx(5.5)
    assert arg_parser.int_or_float_checker(value="5.5", int_min=None, int_max=None, float_min=None, float_max=None) == approx(5.5)
    assert arg_parser.int_or_float_checker(value="5.5", int_min=None, int_max=0, float_min=0, float_max=10) == approx(5.5)
    assert arg_parser.int_or_float_checker(value="5.5", int_min=10, int_max=None, float_min=0, float_max=10) == approx(5.5)

    # float range shouldn't affect int range
    assert arg_parser.int_or_float_checker(value=50, int_min=10, int_max=100, float_min=0, float_max=10) == 50
    assert arg_parser.int_or_float_checker(value="50", int_min=10, int_max=100, float_min=0, float_max=10) == 50
    assert arg_parser.int_or_float_checker(value="50", int_min=10, int_max=None, float_min=0, float_max=10) == 50
    assert arg_parser.int_or_float_checker(value="50", int_min=10, int_max=None, float_min=None, float_max=None) == 50
    assert arg_parser.int_or_float_checker(value="50", int_min=None, int_max=None, float_min=None, float_max=None) == 50
    assert arg_parser.int_or_float_checker(value="50", int_min=None, int_max=None, float_min=0, float_max=None) == 50
    assert arg_parser.int_or_float_checker(value="50", int_min=None, int_max=None, float_min=None, float_max=1) == 50

    # none parsing test
    assert arg_parser.int_or_float_checker(value=None, int_min=10, int_max=100, float_min=0, float_max=10, none_allowed=True) is None
    raises(ArgumentTypeError, arg_parser.int_or_float_checker, value=None, int_min=10, int_max=100, float_min=0, float_max=10, none_allowed=False)

def helper_create_valid_csv_path():
    with open("valid_csv_path.csv", "w") as f:
        f.write("x,y\n1,2\n3,4\n5,6")
    return "valid_csv_path.csv"


# parse main tests

class TempFile:
    def __init__(self, content="x,y\n1,2\n3,4\n5,6", dir="./", suffix=".csv"):
        self.dir = dir
        self.content = content
        self.fd = None
        self.path = None
        self.fd, self.path = mkstemp(suffix=suffix, dir=self.dir)
        
        # Write content to the file
        with fdopen(self.fd, 'w') as f:
            f.write(self.content)

    def __del__(self):
        if self.path and path.exists(self.path):
            remove(self.path)

tmp_csv_file = TempFile()

def test_parse_main_one_param():
    res = arg_parser.parse_main([tmp_csv_file.path, "-sit", "10"])
    assert res["dataset"][0][0] == approx(1)
    assert res["dataset"][0][1] == approx(2)
    assert res["dataset"][1][0] == approx(3)
    assert res["dataset"][1][1] == approx(4)
    assert res["dataset"][2][0] == approx(5)
    assert res["dataset"][2][1] == approx(6)
    assert res["verbose"] == 0
    assert res["export_image"] == True
    assert res["export_csv"] == True
    assert isinstance(res["solver"], arg_parser.EvolutionarySolver)

def test_parse_main_greedy_first():
    res = arg_parser.parse_main([tmp_csv_file.path, "-gf"])
    assert res["dataset"][0][0] == approx(1)
    assert res["dataset"][0][1] == approx(2)
    assert res["dataset"][1][0] == approx(3)
    assert res["dataset"][1][1] == approx(4)
    assert res["dataset"][2][0] == approx(5)
    assert res["dataset"][2][1] == approx(6)
    assert res["verbose"] == 0
    assert res["export_image"] == True
    assert res["export_csv"] == True
    assert isinstance(res["solver"], arg_parser.GreedyFirst)

def test_parse_main_invalid_csv():
    wrong_csv_file = TempFile(content="shouldn't work :)")
    raises(ValueError, arg_parser.parse_main, [wrong_csv_file.path, "-sit", "10"])

    wrong_txt_file = TempFile(suffix=".txt")
    raises(ValueError, arg_parser.parse_main, [wrong_txt_file.path, "-sit", "10"])
