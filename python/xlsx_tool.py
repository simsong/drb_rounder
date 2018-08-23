#!/usr/bin/env xls_tools
#
# A set of tools for working with OpenOffice XML (xlsx files)
#

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile


EXCEL_NAMESPACE = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
SHEET_DATA = EXCEL_NAMESPACE + 'sheetData'
ROW = EXCEL_NAMESPACE + 'row'
C  = EXCEL_NAMESPACE + "c"      # column
V = EXCEL_NAMESPACE + "v"  # value
TR = WORD_NAMESPACE+"tr"                       # table row?
TC = WORD_NAMESPACE+"tc"                       # table cell?

class ExcelFile:
    def __init__(self,fname=None):
        if fname:
            self.read(fname)

    def readWorksheet(self, name):
        xml_content = self.zipfile.read( name )

    def read(self,fname):
        self.filename = fname
        self.zipfile  = zipfile.ZipFile(fname)
        self.worksheets = []
        for name in self.zipfile.namelist():
            if name.startswith("xl/worksheets/"):
                self.worksheets.append( self.readWorksheet( name ))

            print(name)

if __name__=="__main__":
    import sys
    ef = ExcelFile(sys.argv[1])

        
