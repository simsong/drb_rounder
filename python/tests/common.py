#
# test of the helper functions
# Also helper functions for the test suite


import pytest
import sys
import os
import os.path

sys.path.append( os.path.join( os.path.dirname(__file__)))
sys.path.append( os.path.join( os.path.dirname(__file__), ".."))

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "../../test_files" )
WORK_DIR       = os.path.join( os.path.dirname(__file__), "work")

def rm_Rf(workdir):
    """
    Helper function to clear out a given directory if it exists
    """
    if os.path.exists(workdir):
        for (root,dirs,files) in os.walk(workdir,topdown=False):
            for fn in files:
                os.unlink(os.path.join(root,fn))
            for d in dirs:
                os.rmdir(os.path.join(root,d))
        os.rmdir(workdir)

