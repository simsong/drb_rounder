#!/usr/bin/env python36

import py.test
from drb_rounder import * 
import re

def test_nearest():
    assert nearest(80,100) == 100
    assert nearest(120,100) == 100
    assert nearest(51,100) == 100
    assert nearest(51,10) == 50
    assert nearest(56,10) == 60
    assert nearest(60,10) == 60
    assert nearest(61,10) == 60
    

def test_round_str():
    assert round_str("1234")  == "1234"
    assert round_str("12345") == "12340" # ROUND_HALF_EVEN
    assert round_str("12346") == "12350" # ROUND_HALF_EVEN
    assert round_str("123450") == "123400" # ROUND_HALF_EVEN
    assert round_str("123455") == "123500" # ROUND_HALF_EVEN
    assert round_str("123465") == "123500" # ROUND_HALF_EVEN

def test_str_needs_rounding():
    assert str_needs_rounding("1") == False
    assert str_needs_rounding("1,456") == False
    assert str_needs_rounding("123,456") == True
    assert str_needs_rounding("123456") == True


def test_round_float():
    assert round_float(1.0)    == 1.0
    assert round_float(1.2)    == 1.2
    assert round_float(1.23)   == 1.23
    assert round_float(1.234)  == 1.234
    assert round_float(1.2345) == 1.234

    assert round_float(10)    == 10
    assert round_float(12)    == 12
    assert round_float(12.3)   == 12.3
    assert round_float(12.34)  == 12.34
    assert round_float(12.345) == 12.35

def test_find_next_number():
    assert find_next_number("1") == (0,1)
    assert find_next_number("1.") == (0,2)
    assert find_next_number("1.1") == (0,3)
    assert find_next_number("123456") == (0,6)
    assert find_next_number("123,456") == (0,7)
    assert find_next_number(",") == None
    assert find_next_number(" 1, ") == (1,2)

def test_number_re():
    assert number_re.search("1") != None
    assert number_re.search("12") != None
    assert number_re.search(" 1 ") != None
    assert number_re.search(" 12 ") != None
    assert number_re.search(" 123 ") != None
    assert number_re.search(" 1234 ") != None
    assert number_re.search(" 1,234 ") != None
    assert number_re.search(" 11,234 ") != None
    assert number_re.search(" 123,234 ") != None
    assert number_re.search(" 1,123,234 ") != None


def test_numbers_in_line():
    line = " 1 2 3,456 7.890"
    positions = [(1,2), (3,4), (5,10), (11,16)]
    assert numbers_in_line(line) == positions

