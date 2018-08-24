#
# test of the helper functions
# Also helper functions for the test suite


import pytest
import sys
import os
import os.path
import shutil

sys.path.append( os.path.join( os.path.dirname(__file__)))
sys.path.append( os.path.join( os.path.dirname(__file__), ".."))

TEST_FILES_DIR = os.path.join( os.path.dirname(__file__), "../../test_files" )
WORK_DIR       = os.path.join( os.path.dirname(__file__), "work")
WORK2_DIR      = os.path.join( os.path.dirname(__file__), "work2")
DRB_ROUNDER    = os.path.join( os.path.dirname(__file__), "../drb_rounder.py" )

def prep_workdir():
    # Copy all of the files in TEST_FILES_DIR into TEST_FILES_DIR

    if not os.path.exists(WORK_DIR):
        os.mkdir(WORK_DIR)

    for fn in os.listdir(TEST_FILES_DIR):
        ofn = os.path.join(TEST_FILES_DIR, fn)
        nfn = os.path.join(WORK_DIR, fn)
        if not os.path.exists(nfn):
            shutil.copy( ofn, nfn)
            assert os.path.exists(nfn)

