#!/usr/bin/env python3

import pytest
import os
import os.path

from common import TEST_FILES_DIR

from latex_tools import run_latex
from xlsx_info import *
from tytable import HTML, TEXT, LATEX

import subprocess
import shutil

WORK2_DIR = os.path.join( os.path.dirname(__file__), "work2")
XLSX_PATH = os.path.join( TEST_FILES_DIR, "spreadsheet.xlsx")
SPREADSHEET_XLSX=os.path.join(WORK2_DIR, os.path.basename(XLSX_PATH))
SPREADSHEET_TEX=os.path.join(WORK2_DIR, os.path.basename(XLSX_PATH)).replace(".xlsx",".tex")
SPREADSHEET_TXT=os.path.join(WORK2_DIR, os.path.basename(XLSX_PATH)).replace(".xlsx",".txt")


def rm_Rf(workdir):
    # Clear out the workdir
    if os.path.exists(workdir):
        for (root,dirs,files) in os.walk(workdir,topdown=False):
            for fn in files:
                os.unlink(os.path.join(root,fn))
            for d in dirs:
                os.rmdir(os.path.join(root,d))
        os.rmdir(workdir)


def make_workdir(workdir):
    rm_Rf(WORK_DIR)
    os.mkdir(WORK_DIR)
    # copy the files over
    for fn in os.listdir(WEEKLY_TEST_DIR):
        # Do not copy over files beginning with '.'
        if fn[0]=='.': 
            continue
        fnpath = os.path.join(WEEKLY_TEST_DIR,fn)
        shutil.copy(fnpath,WORK_DIR)


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

    rm_Rf(WORK2_DIR)
    os.mkdir(WORK2_DIR)
    shutil.copy(XLSX_PATH, WORK2_DIR)
    print("==>",SPREADSHEET_TEX, SPREADSHEET_TXT)
    with open(SPREADSHEET_TEX,"w") as f:
        f.write("\\documentclass{article}\\begin{document}\n")
        f.write( analyze_xlsx( filename=SPREADSHEET_XLSX, mode=LATEX))
        f.write("\\end{document}\n")
    with open(SPREADSHEET_TXT,"w") as f:
        f.write( analyze_xlsx( filename=SPREADSHEET_XLSX, mode=TEXT))

    run_latex(SPREADSHEET_TEX, repeat=1)


if __name__=="__main__":
    test_analyze_xlsx()
    ret = subprocess.call([sys.executable,'make_combined_file.py',WORK_DIR])
    assert ret==0
