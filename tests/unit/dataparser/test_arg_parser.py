import src.dataparser.arg_parser as arg_parser

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