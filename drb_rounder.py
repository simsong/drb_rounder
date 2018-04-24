#!/usr/bin/env python36

from decimal import Decimal,ROUND_HALF_EVEN,Context
import os
import re

LOGFILE_ROUNDER_EXTENSIONS = ['.log','.txt','.sas']

################################################################
### Rounding codep
################################################################
def round_counts(d):
    if d==0: return d
    if d>=1 and d<=7: return 4
    return d

prec4_rounder = Context(prec=4, rounding=ROUND_HALF_EVEN)
def round_float(f):
    return float(str(prec4_rounder.create_decimal(f)))

def round_decimal(d):
    return float( format( d,'.4g' ))

def round_str(s,add_spaces=True,round_counts=False):
    """Take a string, convert it to a number, and round it. Add spaces if
required. If it is not a number, don't round. Returns as a string.
TK: Currently doesn't put commas back in the numbers."""
    tmp = s

    # Remove the non-digits
    digit_chars = "0123456789.-"
    leading_text = ""
    trailing_text = ""
    while len(tmp)>0 and tmp[0] not in digit_chars:
        leading_text = leading_text + tmp[0]
        tmp = tmp[1:]

    # remove trailing non-digits
    while len(tmp)>0 and tmp[-1] not in digit_chars:
        trailing_text = tmp[-1] + trailing_text
        tmp = tmp[:-1]
    
    # Perform floating point rounding
    # Both of the following are equivalent 
    #rounded = round_decimal(Decimal(tmp))
    rounded = round_float(float(tmp))

    if round_counts and 0 <= rounded <= 7:
        rounded = round_counts(rounded)
    
    rounded_str = str(rounded)
    if "." not in s and rounded_str.endswith(".0"):
        rounded_str = rounded_str[0:-2]
    print("tmp={} Decimal(tmp)={} rounded={} rounded_str={}".format(
            tmp,Decimal(tmp), rounded,rounded_str))

    # Put it back together and return
    ret = leading_text + rounded_str + trailing_text

    if add_spaces:
        # Add missing spaces
        ret += " " * (len(s) - len(ret))
        assert len(s) == len(ret)
    return ret
        
def str_needs_rounding(s):
    """Returns true if a string needs rounding"""
    s = s.replace(",","")       # remove commas
    print("s='{}' round_str(s)='{}'".format(s,round_str(s)))
    return s != round_str(s) 

    
################################################################
### String manipulation code
################################################################

number_re = re.compile(r"\d{1,3}((,\d\d\d)|(\d\d\d))*([.]\d*)?")

def find_next_number(line,pos=0):
    """Find the next number in line, starting at position pos.
    Returns number starting position and length as (start,end)
    or None."""
    m = number_re.search(line[pos:])
    if m:
        span = m.span()
        return (span[0]+pos,span[1]+pos)

def numbers_in_line(line):
    """Returns an array with all of the numbers in the line"""
    ret = []
    pos = 0
    while True:
        loc = find_next_number(line,pos)
        if not loc:
            break
        ret.append(loc)
        pos = loc[1]
    return ret
    
def new_filename(oldfilename):
    # Compute the new filename, which has _rounded before the extension
    (basename,ext) = os.path.splitext(oldfilename)
    return basename+"_rounded" + ext
    

def process_csvfile(infilename):
    """Process a tab or comma-delimited file and create a rounded file"""
    outfilename = new_filename(infilename)
    print("{} --> {}".format(infilename,outfilename))
    line_number = 0
    with open(infilename,"rU") as infile:
        with open(outfilename,"w") as outfile:
            for line in infile:
                stripped_line = line.rstrip()    # remove EOL
                eol_len = len(line) - len(stripped_line)
                eol = line[-eol_len:] # preserve the EOL characters

                line_number += 1
                delimiter = args.delimiter
                if delimiter not in stripped_line:
                    print("No delimiter found in line {}: {}".format(line_number,stripped_line))
                    if " " in stripped_line:
                        print("Using space as delimiter for this line")
                        delimiter = " "

                fields = stripped_line.split(delimiter)
                rounded_fields = [round_str(field) for field in fields]
                outfile.write(delimiter.join(rounded_fields))
                outfile.write(eol) # output the original eol
    print("Lines processed: {}".format(line_number))

def process_xlsx(path):
    from openpyxl import load_workbook
    wb = load_workbook(path)
    for sheetname in wb.sheetnames:
        sheet = wb.get_sheet_by_name(sheetname)
        for cell in sheet.get_cell_collection():
            if type(cell.value)==int:
                pass
    print(dir(wb))

HTML_HEADER="""<html>
<head>
<style>
.before {
  color: red;
  background-color: yellow;
}
</style>
</head>
<body>
<pre>
"""

HTML_FOOTER="""</pre>
</body>
</html>
"""


def process_logfile(fname):
    # Make sure that our intended output files do not exist
    (name,ext) = os.path.splitext(fname)
    fname_rounded = name + "_rounded" + ext
    
    # before - highlight items that need rounding
    fname_before  = name + "_0.html"
    fbefore = open(fname_before,"w")
    fbefore.write(HTML_HEADER)

    # after - show it rounded
    fname_after  = name + "_1.html"
    fafter = open(fname_after,"w")
    fafter.write(HTML_HEADER)

    with open(fname) as fin:
        for line in fin:
            pos = 0             # where we are on the line
            before = []
            spans = numbers_in_line(line)
            for span in spans:
                num = float(line[ span[0] : span[1] ])
                
                before.append( line[ pos : span[0]] ) # part of line before span in question
                before.append("<span class='before'>")
                before.append( line[ span[0] : span[1]] ) #  span in question
                before.append("</span>")
                pos = span[1]
            before.append( line[ pos: ] ) # get end of line (or entire line, if not spans)
            fbefore.write("".join(before))
    fbefore.write(HTML_FOOTER)

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Perform DRB-style rounding',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('files', type=str, nargs='+', help='File[s] to round')
    parser.add_argument("--tab",action="store_true",help="Assume CSV is tab delimited")
    parser.add_argument("--log",help="Invoke logfile rounder. This is the default for files ending in {}".format(" ".join(LOGFILE_ROUNDER_EXTENSIONS)))
    parser.add_argument("--counts",help="Apply rounding rules for small counts: 0-7 rounds to 4",action='store_true')
    args = parser.parse_args()
    args.delimiter = "\t"       # default delimiter
    for fname in args.files:
        if args.log:
            process_logfile(fname)
            continue

        (base,ext) = os.path.splitext(fname)
        ext = ext.lower()
        if ext == ".xlsx":
            process_xlsx(fname)
        elif ext in ['.csv','.tsv']:
            process_csvfile(fname)
        elif ext in LOGFILE_ROUNDER_EXTENSIONS:
            process_logfile(fname)
        else:
            print("Don't know how to process '{}' type file in: {}".format(ext,fname),out=sys.stderr)
            exit(1)
