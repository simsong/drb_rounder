#
# Support tools for datafiles (xls, xlsx, csv, etc.)
#
# it would be nice to be able to just use pandas, but that doesn't support styling and editing XLS files

# Referneces:
# https://www.blog.pythonlibrary.org/2014/03/24/creating-microsoft-excel-spreadsheets-with-python-and-xlwt/

#
# This class provides the following functions. Most of them are passthroughs.
# Datafile() - opens the file
#  sheets - returns list of the sheets.
#  sheet(s) - returns the sheet
#  sheetrow(x,r) - returns the values in the row
#  cell(sheet,row,col)


import xlrd
import xlwt

def main():
    """"""
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("PySheet1")
 
    cols = ["A", "B", "C", "D", "E"]
    txt = "Row %s, Col %s"
 
    for num in range(5):
        row = sheet1.row(num)
        for index, col in enumerate(cols):
            value = txt % (num+1, col)
            row.write(index, value)
 
    book.save("test.xls")
    book.save("test.xlsx")
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    main()
