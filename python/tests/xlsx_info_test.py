#!/usr/bin/env python3

import pytest
import os
import os.path

from common import *

from latex_tools import run_latex
from xlsx_info import *
from tytable import HTML, TEXT, LATEX

import subprocess
import shutil

XLSX_PATH = os.path.join( TEST_FILES_DIR, "spreadsheet.xlsx")
SPREADSHEET_XLSX=os.path.join(WORK2_DIR, os.path.basename(XLSX_PATH))
SPREADSHEET_TEX=os.path.join(WORK2_DIR, os.path.basename(XLSX_PATH)).replace(".xlsx",".tex")
SPREADSHEET_TXT=os.path.join(WORK2_DIR, os.path.basename(XLSX_PATH)).replace(".xlsx",".txt")


def test_find_sigfigs():
    assert SigFigStats.find_sigfigs(0) == 0
    assert SigFigStats.find_sigfigs(1) == 1
    assert SigFigStats.find_sigfigs(2) == 1
    assert SigFigStats.find_sigfigs(1.1) == 2
    assert SigFigStats.find_sigfigs(1.23) == 3
    assert SigFigStats.find_sigfigs(12.3) == 3
    assert SigFigStats.find_sigfigs(123.) == 3
    assert SigFigStats.find_sigfigs("0") == 0
    assert SigFigStats.find_sigfigs("1") == 1
    assert SigFigStats.find_sigfigs("2") == 1
    assert SigFigStats.find_sigfigs("1.1") == 2
    assert SigFigStats.find_sigfigs("1.23") == 3
    assert SigFigStats.find_sigfigs("12.3") == 3
    assert SigFigStats.find_sigfigs("123.") == 3


def test_analyze_xlsx():
    """ This just test to make sure that the LaTeX file created can be processed."""
    assert SPREADSHEET_TEX != SPREADSHEET_TXT

    if not os.path.exists(WORK2_DIR):
        os.mkdir(WORK2_DIR)
    shutil.copy(XLSX_PATH, WORK2_DIR)
    print("==>",SPREADSHEET_TEX, SPREADSHEET_TXT)
    with open(SPREADSHEET_TEX,"w") as f:
        f.write("\\documentclass{article}\\begin{document}\n")
        f.write( analyze_file( filename=SPREADSHEET_XLSX, mode=LATEX))
        f.write("\\end{document}\n")
    with open(SPREADSHEET_TXT,"w") as f:
        f.write( analyze_file( filename=SPREADSHEET_XLSX, mode=TEXT))

    run_latex(SPREADSHEET_TEX, repeat=1)


