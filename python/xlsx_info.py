#!/usr/bin/env python3

"""
Prepare a report of disclosure avoidance statistics about an excel spreadsheet.
Output can be in HTML, TEXT or LATEX.
Can be run stand-alone or within the combined file printer.
"""

from openpyxl import load_workbook
from openpyxl.cell.read_only import EmptyCell
from collections import defaultdict
import zipfile
import tytable
from tytable import ttable, HTML, TEXT, LATEX

from latex_tools import latex_escape, textbf, nl

import os
import os.path
import re
import sys
sigfig_re = re.compile("([0-9.]+)")

ALERT_DIGITS = 5                # alert if this many digits or more
ALERT_VALUES = 10               # alert on this many values

def colname(col):
    assert 0<=col<=26+26*26     # only handles 1 and 2 character cols

    col -= 1                    # column 0 is A
    if col<26:
        return chr( ord("A") + col)
    r1 = (col-26) // 26
    r2 = (col-26) % 26
    return colname(r1) + colname(r2)

def improperly_rounded(val):
    return SigFigStats.find_sigfigs(val) >= ALERT_DIGITS


class ProblemStat:
    def __init__(self,*,sheet="",row="",col="",source="xls"):
        self.sheet = sheet
        self.row   = row
        self.col   = col
        self.source  = source

    def __lt__(self,v):
        if self.row < v.row: return True
        if self.row > v.row: return False
        if self.col < v.col: return True
        return False
        
    def __le__(self,v):
        if self.row <= v.row: return True
        if self.row > v.row: return False
        if self.col <= v.col: return True
        return False
        
    def __str__(self):
        if self.source=="xls":
            if self.sheet:
                return "{}:{}{}".format(self.sheet,colname(self.col),self.row)
            return "{}{}".format(colname(self.col),self.row)

class SigFigStats:
    """Maintain statistics about improperly rounded values"""
    @staticmethod
    def find_sigfigs(x):
        """Odd little function to return the number of significant figures in a number"""
        # Kill everything to the right of the e and remove the period
        m = sigfig_re.search("{:e}".format(float(x)))
        if m:
            val = m.group(1).replace(".","")
            while val[-1:]=='0':
                val = val[0:-1]
            return len(val)
        return 0                    # no significant figures if it can't be made scientific

    def __init__(self):
        self.max_row = 0
        self.max_col = 0
        self.sig_digits_histogram = defaultdict(int) # count
        self.sig_digits_alerts    = defaultdict(list)
        self.count = 0
        self.improper_count = 0

    def add(self,*, val, row, col):
        """Adds a number to the counter and return True if it has more than ALERT_DIGITS significant figures"""
        sigfigs = SigFigStats.find_sigfigs(val)
        self.max_row = max(self.max_row, row)
        self.max_col = max(self.max_col, col)
        self.sig_digits_histogram[sigfigs] += 1
        self.count += 1
        if improperly_rounded(val):
            self.improper_count += 1
            self.sig_digits_alerts[sigfigs].append(ProblemStat(row=row,col=col))

    def typeset(self,*,mode):
        if not self.count:
            return ""
        t = ttable()
        t.add_head(['Significant Digits','Cell count','Problem cells'])
        t.set_latex_colspec("rrl")
        t.set_col_alignment(1,ttable.CENTER)
        for (sig_digs,vals) in sorted(self.sig_digits_alerts.items()):
            alert_cells = sorted(vals)[0:ALERT_VALUES]
            alerts = " ".join( [str(a) for a in alert_cells])
            if len(alert_cells) >= ALERT_VALUES:
                alerts += r" . . . "
            t.add_data( (sig_digs,len(vals),alerts) )
        if t.data:
            return t.typeset(mode=mode)
        else:
            return ""
    
def analyze_xlsx(*,filename,mode=TEXT):
    """Analyze the named excel spreadsheet and return a string in the specified format."""
    ret = []                    # an array of strings to be joined and returned
    NL = tytable.line_end(mode)
    if mode==TEXT:
        ret += [filename,'\n',"="*len(filename),NL]
    elif mode==LATEX:
        ret += [textbf(latex_escape(filename+":")),NL]
        
    try:
        wb = load_workbook(filename=filename, read_only=True)
    except zipfile.BadZipFile:
        ret += ['Cannot read; badZipFile',NL]
        return "".join(ret)
    except TypeError:
        ret += ['Cannot read; bad Excel File',NL]
        return "".join(ret)

    tt = ttable()
    tt.add_head(['',
                 'Worksheet Name','rows with data','columns with data',
                 'total numeric values','cells with $>4$ sigfigs'])
    
    for i in range(len(wb.worksheets)):
        ws   = wb.worksheets[i]
        sb_ws = SigFigStats()              # for this worksheet
        
        empty_cells = 0
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell,EmptyCell):
                    empty_cells += 1
                    continue
                try:
                    if cell.value==None:
                        continue
                    val = float(cell.value)
                except (ValueError,TypeError,OverflowError) as e:
                    continue
                sb_ws.add(val=val, row=cell.row, col=cell.column)
        ret += ["Worksheet "+ws.title] + [""] + [sb_ws.typeset(mode=mode)]
        tt.add_data([i+1,latex_escape(ws.title),sb_ws.max_row,sb_ws.max_col,sb_ws.count, sb_ws.improper_count])
        # End of worksheet processing

    tt.set_col_totals([4,5])
    ret = [tt.typeset(mode=mode)] + ret + [""]

    # count the number of numbers and their precision
    return "\n".join(ret)

def analyze_csv(*,filename,mode=TEXT):
    """Analyze the numbers in a text file"""
    ret = []
    NL = tytable.line_end(mode)
    if mode==TEXT:
        ret += [filename,'\n',"="*len(filename),NL]
    elif mode==LATEX:
        ret += [textbf(latex_escape(filename+":")),NL]
    div = re.compile("[ ,]")
    sb = SigFigStats()
    with open(filename,"r") as f:
        row_number = 0
        for line in f:
            row_number += 1
            col_number = 0     
            for word in div.split(line):
                try:
                    val = float(word)
                    sb.add(val=val,row=row_number,col=col_number)
                except (ValueError,TypeError,OverflowError) as e:
                    pass
                col_number += 1
    ret += ["rows: {}  columns: {}  numbers: {}".format(sb.max_row,sb.max_col,sb.count),NL]
    ret += [sb.typeset(mode=mode)]
    return "\n".join(ret)

def can_analyze_file(*,filename):
    return filename.endswith(".xlsx") or filename.endswith(".csv")

def analyze_file(*,filename,mode=TEXT):
    (base,ext) = os.path.splitext(filename)
    if ext=='.xlsx':
        return analyze_xlsx(filename=filename,mode=mode)
    elif ext=='.csv':
        return analyze_csv(filename=filename,mode=mode)
    raise RuntimeError("{}: Unknown file type: {}".format(filename,ext))

def mytest_annotate(fname):
    from openpyxl import load_workbook
    from openpyxl.comments import Comment
    from openpyxl.styles import Color, PatternFill, Font, Border

    wb = load_workbook(fname)
    ws = wb.active
    redFill = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')

    ws['A1'].comment = Comment("Comment for A1","No Such Author")
    ws['A2'].fill = redFill
    (base,ext) = os.path.splitext(fname)
    wb.save(base+"-new"+ext)
 

if __name__=="__main__":
    from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
    parser = ArgumentParser( formatter_class = ArgumentDefaultsHelpFormatter )
    parser.add_argument("file",help="file to analyze")
    parser.add_argument("--test", help="Test a file by making minor modificaitons to it.", action='store_true')
    parser.add_argument("--debug", action='store_true')
    parser.add_argument("--text", action='store_true')
    parser.add_argument("--latex", action='store_true')
    args = parser.parse_args()

    if args.test:
        mytest_annotate(args.file)
        exit(1)

    if not args.text and not args.latex:
        args.text = True

    if args.text:
        print(analyze_file(filename=args.file,mode=TEXT))
        print("")

    if args.latex:
        print(analyze_file(filename=args.file,mode=LATEX))
        print("")
