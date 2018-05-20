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
    
def test_round_counts():
    assert round_counts(1) == "<15"
    assert round_counts(14) == "<15"
    assert round_counts(15) == "20"
    assert round_counts(20) == "20"
    assert round_counts(24) == "20"
    
def test_round4_float():
    assert round_str(1234.)  == 1234.
    assert round_str(12345.) == 12340.
    assert round_str(12346.) == 12350. 
    assert round_str(123450.) == 123400. 
    assert round_str(123455.) == 123500. 
    assert round_str(123465.) == 123500. 


def test_round_str():
    # Counts
    assert round_str("1234")  == "1200"
    assert round_str("12345") == "12500" # ROUND_HALF_EVEN
    assert round_str("12346") == "12500" # ROUND_HALF_EVEN
    assert round_str("123450") == "123000" # ROUND_HALF_EVEN
    assert round_str("123455") == "123000" # ROUND_HALF_EVEN
    assert round_str("123465") == "123000" # ROUND_HALF_EVEN

    # decimals
    assert round_str("1234.")  == "1234."
    assert round_str("12345.") == "12340." # ROUND_HALF_EVEN
    assert round_str("12346.") == "12350." # ROUND_HALF_EVEN
    assert round_str("123450.") == "123400." # ROUND_HALF_EVEN
    assert round_str("123455.") == "123500." # ROUND_HALF_EVEN
    assert round_str("123465.") == "123500." # ROUND_HALF_EVEN

def test_determine_rounding_method():
    assert determine_rounding_method("1,456") == COUNTS_METHOD
    assert determine_rounding_method("1,456.") == ROUND4_METHOD

def test_analyze_for_rounding():
    # Check a number of case as both counts and floats
    # Check as count data

    assert analyze_for_rounding("1")[NEEDS_ROUNDING] == True # becomes <15
    assert analyze_for_rounding("1")[ROUNDED] == "<15"
    assert analyze_for_rounding("1,456")[NEEDS_ROUNDING] == True
    assert analyze_for_rounding("1,456")[ROUNDED] == "1,500"
    assert analyze_for_rounding("123,456")[NEEDS_ROUNDING] == True
    assert analyze_for_rounding("123,456")[ROUNDED] == "123,000"
    assert analyze_for_rounding("123456")[NEEDS_ROUNDING] == True
    assert analyze_for_rounding("123456")[ROUNDED] == "123000"

    # Check as floats

    assert analyze_for_rounding("1.")[NEEDS_ROUNDING] == False
    assert analyze_for_rounding("1,456.")[NEEDS_ROUNDING] == False
    assert analyze_for_rounding("123,456.")[NEEDS_ROUNDING] == True
    assert analyze_for_rounding("123,456.")[ROUNDED] == "123,500."
    assert analyze_for_rounding("123456.")[NEEDS_ROUNDING] == True
    assert analyze_for_rounding("123456.")[ROUNDED] == "123500."


def test_round4_float():
    assert round4_float(1.0)    == 1.0
    assert round4_float(1.2)    == 1.2
    assert round4_float(1.23)   == 1.23
    assert round4_float(1.234)  == 1.234
    assert round4_float(1.2345) == 1.234

    assert round4_float(10)    == 10
    assert round4_float(12)    == 12
    assert round4_float(12.3)   == 12.3
    assert round4_float(12.34)  == 12.34
    assert round4_float(12.345) == 12.35

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

