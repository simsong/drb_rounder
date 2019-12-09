import pytest
import sys
import os
import os.path

from common import *

import number

ROUND4_METHOD="round4"
COUNTS_METHOD="counts"
LESS_THAN_15 = "<15"

rounding_info = {
    'original': None,
    'original_cleaned': None,
    'rounded_cleaned': None,
    'rounded': None,
    'leading_text': None,
    'trailing_text': None,
    'has_commas': None,
    'in_scientific_form': None,
    'method': None,
    'needed_rounding': None
}


def test_clean():
    # 9 current test cases
    original           = ["1234", "123,456", "(0.3456)", "(.12345678)", "12/12/1225", "hello world", "/123.4567/", "12345E+06", "-1234"]
    original_cleaned   = ["1234", "123456", "0.3456", ".12345678", "12/12/1225", "", "123.4567", "12345000000", "1234"]
    leading_text       = ["", "", "(", "(", "", "hello world", "/", "", "-"]
    trailing_text      = ["", "", ")", ")", "", "", "/", "", ""]
    has_commas         = [False, True, False, False, False, False, False, False, False]
    in_scientific_form = [False, False, False, False, False, False, False, True, False]

    for i in range(len(original)):
        num = number.Number(original[i])
        num.clean()

        assert num.original == original[i]
        assert num.original_cleaned == original_cleaned[i]
        assert num.leading_text == leading_text[i]
        assert num.trailing_text == trailing_text[i]
        assert num.has_commas == has_commas[i]
        assert num.in_scientific_form == in_scientific_form[i]


def test_reconstruct():
    """
    This function will only test inputs that abide by the following rules:
       - there are NO alphabetical letters in the cleaned string
       - the cleaned string is NOT an empty string
       - there are NO symbols found in the cleaned string

    The reconstruct function will only be called when those conditions are true
    """
    # 6 current test cases
    original           = ["1234", "123,456", "(0.3456)", "(.12345678)", "/123.4567/", "1.234+e2"]
    original_cleaned   = ["1234", "123456",  "0.3456",   ".12345678",   "123.4567",   "123.4"]
    rounded_cleaned    = ["1200", "123000",  "0.3456",   "0.1235",      "123.5",      "1.234E+02"]
    rounded            = ["1200", "123,000", "(0.3456)", "(0.1235)   ", "/123.5/   ", "1.234E+02"]
    leading_text       = ["",     "",        "(",        "(",           "/",          ""]
    trailing_text      = ["",     "",        ")",        ")",           "/",          ""]
    has_commas         = [False,  True,      False,      False,         False,        False]
    method             = [COUNTS_METHOD, COUNTS_METHOD, ROUND4_METHOD, ROUND4_METHOD, ROUND4_METHOD, ROUND4_METHOD]
    in_scientific_form = [False,  False,     False,      False,         False,        True]

    for i in range(len(original)):
        ri = dict(rounding_info)
        ri['original'] = original[i]
        ri['original_cleaned'] = original_cleaned[i]
        ri['rounded_cleaned'] = rounded_cleaned[i]
        ri['leading_text'] = leading_text[i]
        ri['trailing_text'] = trailing_text[i]
        ri['has_commas'] = has_commas[i]
        ri['method'] = method[i]
        ri['in_scientific_form'] = in_scientific_form[i]

        num = number.Number(None)
        num.init_for_testing(ri)
        num.reconstruct()
        assert num.rounded == rounded[i]


def test_round():
    """
    This function will only check the changes in special features:
        - original value
        - whether the value needs rounding (bool)
        - rounded value

    All other test cases should handle the inner workings of the rounder
    """
    # 6 current test cases
    original       = ["1234", "123,456", "(0.3456)", "(.12345678)", "/123.4567/", "1.2345e-5", "-1234"]
    rounded        = ["1200", "123,000", "(0.3456)", "(0.1235)   ", "/123.5/   ", "1.234E-05", "-1200"]
    needed_rounding = [True, True, False, True, True, True, True, True]

    for i in range(len(original)):
        num = number.Number(original[i])
        num.round()

        assert num.original == original[i]
        assert num.needed_rounding == needed_rounding[i]
        assert num.rounded == rounded[i]
