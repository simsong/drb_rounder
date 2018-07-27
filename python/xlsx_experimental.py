#!/usr/bin/env python3

import pandas as pd
import numpy as np
from xlsxwriter.utility import xl_rowcol_to_cell

# Apparently we can use pandas to read and write xls files.
# And to color them.
# http://pbpython.com/improve-pandas-excel-output.html
def try1():
    # Output file looks really different from input file. Ick.
    df = pd.read_excel("../test_files/test_spreadsheet2.xlsx")
    writer_orig = pd.ExcelWriter('outputa.xlsx', engine='xlsxwriter')
    df.to_excel(writer_orig, index=False, sheet_name='demo')
    writer_orig.save()

# https://stackoverflow.com/questions/10532367/how-to-change-background-color-of-excel-cell-with-python-xlwt-library/10542220
def try2():
    from xlwt import Workbook
    import xlwt
    book = Workbook()
    sheet1 = book.add_sheet('Sheet 1')
    book.add_sheet('Sheet 2')
    for i in range(0, 100):
        st = xlwt.easyxf('pattern: pattern solid;')
        st.pattern.pattern_fore_colour = i
        sheet1.write(i % 24, i // 24, 'Test text',st)
    book.save('simple.xls')

# https://stackoverflow.com/questions/26957831/edit-existing-excel-workbooks-and-sheets-with-xlrd-and-xlwt
def try3():
    from xlrd import open_workbook
    from xlwt import Workbook
    import xlwt
    from xlutils.copy import copy
    w = copy("../test_files/test_spreadsheet2.xls")
    wb = open_workbook("../test_files/test_spreadsheet2.xls")
    print("wb=",wb,"type(wb)=",type(wb),"Workbook=",Workbook)
    #print(dir(wb))
    print(wb.sheets())
    #s = wb.get_sheet(0)
    s = wb.sheets()[0]
    st = xlwt.easyxf('pattern: pattern solid;')
    st.pattern.pattern_fore_colour = 20
    print(dir(s))
    s.write(0,0,'A1',st)
    wb.save('names.xls')

#Other things to try:
# https://stackoverflow.com/questions/2725852/writing-to-existing-workbook-using-xlwt
# http://kitchingroup.cheme.cmu.edu/blog/2013/03/08/Interacting-with-Excel-in-python/
# https://stackoverflow.com/questions/26957831/edit-existing-excel-workbooks-and-sheets-with-xlrd-and-xlwt
# http://xlsxwriter.readthedocs.io/working_with_colors.html
# http://xlsxwriter.readthedocs.io/format.html
# http://xlsxwriter.readthedocs.io/index.html
# https://www.penwatch.net/cms/excel_cell_bg_color/
# https://stackoverflow.com/questions/16560289/using-python-write-an-excel-file-with-columns-copied-from-another-excel-file
# Here are some options to choose from:
# xlwt (writing xls files)
# xlrd (reading xls/xlsx files)
# openpyxl (reading/writing xlsx files)
# xlsxwriter (writing xlsx files)
# Looks like openpyxl is the one to use
# https://pythonhosted.org/openpyxl/

# but this is a tutorial that does it with xlrd and xlwt:
# https://www.programering.com/a/MTMyQDNwATU.html


if __name__=="__main__":
    try3()

# This isn't used anymore:
"""
    import xml.etree.ElementTree as ET
    from xml.etree.ElementTree import XML
    import zipfile
    SPREADSHEET_NAMESPACE = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
    CELL  = SPREADSHEET_NAMESPACE + 'c'
    VALUE = SPREADSHEET_NAMESPACE + 'v'
    FORMULA  = SPREADSHEET_NAMESPACE + "f"
    document = zipfile.ZipFile(path)
    xml_content = document.read('xl/worksheets/sheet1.xml')
    document.close()
    #tree = XML(xml_content)
    root = ET.fromstring(xml_content)
    print("BEFORE:",xml_content)
    print("root.tag:",root.tag)
    for cell in root.getiterator(CELL):
        children = cell.getchildren()
        formulas = list(filter(lambda child:child.tag==FORMULA,children))
        values   = list(filter(lambda child:child.tag==VALUE,children))
        
        if not formulas and len(values)==1:
            ov = values[0].text
            values[0].text = round_str(values[0].text)
            nv = values[0].text
            print("value: {} --> {}".format(ov,nv))
            continue

        if len(formulas)==1 and len(values)==1:
            # Delete the value
            cell.remove(values[0])

        print(dir(cell))
        print("=======")
    print("AFTER:",dir(root))
    print(ET.dump(root))
"""

