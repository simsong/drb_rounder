#!/usr/bin/env python36

from decimal import Decimal,ROUND_HALF_EVEN,Context
import os
import re
import math

LOGFILE_ROUNDER_EXTENSIONS = ['.log','.txt','.sas']

################################################################
### Rounding code
################################################################
def nearest(n, range):
    return math.floor((n / range) + 0.5) * range

def round_counts(n):
    """Implements the DRB rounding rules for counts. Note that we return a string, 
    so that we can report N < 15"""
    assert n == math.floor(n)    # make sure it is an integer!
    assert n >= 0
    if 0 <= n < 15: return "< 15"
    if 15 <= n <= 99: return str(nearest( n, 10))
    if 100 <= n <= 999: return str(nearest( n, 50))
    if 1000 <= n <= 9999: return str(nearest( n, 100))
    if 10000 <= n <= 99999: return str(nearest( n, 500))
    if 100000 <= n <= 999999: return str(nearest( n, 1000))
    return round_decimal( n )


prec4_rounder = Context(prec=4, rounding=ROUND_HALF_EVEN)
def round_float(f):
    return float(str(prec4_rounder.create_decimal(f)))

def round_decimal(d):
    return float( format( d,'.4g' ))

def str_to_float(s):
    """Convert a string to a float"""
    return float( s.replace(",",""))

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

    # If the original string had commas, add them back
    # Otherwise just change the rounded number to a string
    if "," in s:
        rounded_str = "{:,}".format(rounded)
    else:
        rounded_str = "{:}".format(rounded)

    # If the original string had no ".", make sure that the new string has no "."
    if ("." not in s) and ("." in rounded_str):
        rounded_str = rounded_str[0: rounded_str.find(".")]
        
    # If the original string ended in ".", make sure that the new string ends in "."
    if (s.endswith(".")) and (not rounded_str.endswith(".")) and ("." in rounded_str):
        rounded_str = rounded_str[0: rounded_str.find(".")+1]

    print("tmp={} Decimal(tmp)={} rounded={} rounded_str={} leading_text={} training_text={}".format(
            tmp,Decimal(tmp), rounded,rounded_str, leading_text, trailing_text))

    # Put it back together and return
    ret = leading_text + rounded_str + trailing_text

    if add_spaces:
        # Add missing spaces
        ret += " " * (len(s) - len(ret))
        print("s={} ret={}".format(s,ret))
        assert len(s) == len(ret)
    return ret
        
def str_needs_rounding(s,return_rounded = False):
    """Check to see if s needs rounding. If so, return True, but if return_rounded is true, return the rounded values."""
    s = s.replace(",","")       # remove commas
    rounded_str = round_str(s)
    if s == rounded_str:
        return False
    if return_rounded:
        return rounded_str
    return True

    
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
    
################################################################
### filename code
################################################################

def safe_open(filename,mode,return_none=False):
    """Like open, but if filename exists and mode is 'w', produce an error"""
    if 'w' in mode and os.path.exists(filename):
        print("***************************************")
        print("OUTPUT FILE EXISTS: {}".format(filename))
        print("Please delete or rename file and restart program.")
        if return_none:
            return None
        exit(1)
    return open(filename,mode)


def process_csvfile(infilename):
    """Process a tab or comma-delimited file and create a rounded file"""
    (basename,ext) = os.path.splitext(oldfilename)
    outfilename = basename+"_rounded"+ext
    print("{} --> {}".format(infilename,outfilename))
    line_number = 0
    with open(infilename,"rU") as infile:
        with safe_open(outfilename,"w") as outfile:
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
.after {
  color: black;
  background-color: LightGreen;
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
    frounded = safe_open(fname_rounded, "w", return_none=True)
    
    # before - highlight items that need rounding
    fname_before  = name + "_0.html"
    fbefore = safe_open(fname_before, "w", return_none=True)

    # after - show it rounded
    fname_after  = name + "_1.html"
    fafter = safe_open(fname_after, "w", return_none=True)

    if (not frounded) or (not fbefore) or (not fafter):
        print("PROGRAM HALTS")
        exit(1)

    fbefore.write(HTML_HEADER)
    fafter.write(HTML_HEADER)

    # Note that the output was rounded

    frounded.write("*** THIS FILE HAS BEEN ROUNDED TO 4 SIGNIFICANT DIGITS ***\n")
    fbefore.write("<p><b>*** THIS FILE HAS BEEN ROUNDED TO 4 SIGNIFICANT DIGITS ***</b></p>\n")
    fafter.write("<p><b>*** THIS FILE HAS BEEN ROUNDED TO 4 SIGNIFICANT DIGITS ***</b></p>\n")


    with open(fname) as fin:
        for line in fin:
            pos = 0             # where we are on the line
            rounded = []
            before = []
            after  = []
            spans = numbers_in_line(line)
            for span in spans:
                rounded_str = str_needs_rounding(line[ span[0] : span[1] ], return_rounded=True)
                if rounded_str:
                    before.append( line[ pos : span[0]] ) # part of line before span in question
                    before.append("<span class='before'>")
                    before.append( line[ span[0] : span[1]] ) #  span in question
                    before.append("</span>")

                    after.append( line[ pos : span[0]] ) # part of line after span in question
                    after.append("<span class='after'>")
                    after.append( rounded_str ) #  span in question
                    after.append("</span>")

                    rounded.append( line[ pos : span[0]] )
                    rounded.append( rounded_str )

                    pos = span[1] # next character on line to process is span[1]
                    
            # get end of line (or entire line, if not spans)
            before.append( line[ pos: ] )  
            after.append( line[ pos: ] ) 
            rounded.append( line[ pos: ] ) 

            fbefore.write("".join(before))
            fafter.write("".join(after))
            frounded.write("".join(rounded))
            
    fbefore.write(HTML_FOOTER)
    fafter.write(HTML_FOOTER)

    frounded.close()
    fbefore.close()
    fafter.close()

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
