# DRB Rounding Tools
Simson L. Garfinkel, US Census Bureau
September 2019

The US Census Bureau Disclosure Review Board has adopted a set of
interium data release rules that require all statistics produced from
confidential data sources to be "rounded" to a reduced level of
prevision.  These rules provide some protection against disclosure of
information traceable to individuals, but do not provide privacy
protection that is formally provable. The rounding rules are an
interim solution for privacy protection, but the plan is to replace
them with a system that is formally private at some point in the
future.

## Rounding Rules

There are two DRB rounding rules:

For __counts__:

  * If N is less than 15, report N<15
  * If N is between 15 and 99, round to the nearest 10
  * If N is between 100-999, round to the nearest 50
  * If N is between 1000-9999, round to the nearest 100
  * If N is between 10000-99999, round to the nearest 500
  * If N is between 100000-999999, round to the nearest 1,000
  * If N is 1000000 or more, round to four significant digits

For all numbers (both integer and floating point):

  * All values must be rounded to a maximum of four significant
  figures. (e.g. 1.234 x 10**n).

Note that rounding should implement the (IEEE floating point rounding
rules)[https://en.wikipedia.org/wiki/IEEE_754#Rounding_rules] with the
"round half even" option when rounding. This means that 1000.5 rounds
to 1000 while 1001.5 rounds to 1002.

## Software in this Repo
This git repo contains software that have been created that implement the
rouding rules. These tools include:

* python/drb_rounder.py --- A Python program that applies both the
  rules for counts and regarding the number of significant figures to
  input files that are in CSV or XLSX format.

* sas/rounding_counts.sas --- A SAS procedure for applying the
  generalization to counts.

* sas/rounding_params.sas --- A SAS procedure for applying the
  coarsening to parameters (i.e. floating point values).

* stata/rounding_N.do --- A Stata DO file for applying rules for
  counts.

* stata/rounding_4sigdig.do --- A Stata DO file for applying the rules
  requiring rounding to 4 significant digits.

# The python drb_rounder

The `drb_rounder.py` is a python3 program that implements the rounding rules for the
U.S. Census Bureau's Disclosure Review Board (DRB). This program is the
primary tool that the DRB makes available to researchers needing to
apply the rounding rules to a output prior to review by a disclosure
avoidance officer (DAO) or the DRB.

The program is designed to be easy to use. Specifically:

1. Input is accepted in a wide variety of formats.
2. Data output is in the same format as the input.
3. In addition to the data output, the program produces a report of what numbers were rounded and which were left as-is.
4. The program can be imported as a module in other python programs, allowing the rules to be applied directly by the researcher in another Python program.


## Input formats

The `drb_rounder.py` accepts input in many formats:

* Free Text Input [.txt, .log, .sas, .lst, .tex, .py, .r]
* Comma / Tab Separated Values [.csv, .tsv]
* Spreadsheets [.xlsx, .xls, .ods]
* Documents [.docx, .odt]

## Running the DRB Rounder on Free Text Input
Currently, the rounder is a Python3 program that must be run from the Unix or Windows command line.
(Note that `python3` must be in your path:)

To run, use this command:

```sh
python3 drb_rounder.py filename.xxx
```

Where `filename.xxx` is the name of the text file containing the results to be
rounded.

This will produce three output files:
  * `filename_rounded.xxx` --- The file with the rounded data
  * `filename_0.html` --- An HTML file showing the original data, with
  annotations on the values that require rounding.
  * `filename_1.html`--- An HTML file showing the rounded data, with
  annotations to indicate what was rounded.

If you open both of the HTML files in different tabs of a web browser, you can
easily toggle between the two views:

<img src='pics/input0.png'> <img src='pics/input1.png'>

## Running the DRB Rounder on a delimited file

If you are rounding a delimited data file (for example, a comma-separated values file), the rounder will do a better job if you tell it of the file format.

If you are using a CSV file, the rounder will infer that the file is comma-separated from the file extension:

```sh
python3 drb_rounder.py filename.csv
```

However, if your CSV file is a tab-separated file, be sure to use the `--tab` command-line option to tell the rounder to adjust its behavior:

```sh
python3 drb_rounder.py filename.csv --tab
```

## Running the DRB Rounder on an Excel Spreadsheet
To use the rounder, run the following from the Unix or Windows command line.
NOTE the following:
  * `python3` must be in your path:
  * all .xls and .ods files will be converted to .xlsx if you're running this
  on a windows machine
  * if a cell has alphabetical symbols in it, rounding will not be applied to
  that cell (i.e. Year: 2018)
  * if a cell has any non-digit symbols between digit values, rounding will not
  be applied to that cell (i.e. 06/27/2018)
  * rounding rules are applied to the actual value of the cell, and not the 
  value that is solely displayed by excel formatting

```sh
python3 drb_rounder.py filename.xlsx
```
If you don't want the rounder to actually round the improperly rounded cells and
only highlight these cells, pass the highlight flag as shown below.

```sh
python3 drb_rounder.py filename.xlsx --highlight


These commands will generate a new spreadsheet `filename_rounded.xlsx` which
will contain all of the rounded values.
  * All blue colored cells represent an integer that was rounded
  * All orange colored cells represent a float that was rounded

<img src='pics/xlsx_input.png'> <img src='pics/xlsx_output.png'>


## Running the DRB Rounder without an installation of Python
We've packaged all of the source code and its dependencies so that you don't
need an installation of python to run the rounder. NOTE: the executable is
located in CED's shared drive under M:\Users\Thomas

To run the executable, simply enter the following from the project's root 
directory:

```sh
./drb-rounder-executable/dist/drb_rounder/drb_rounder.exe <test_filename_here>
```

or if you're using command prompt on windows, run

```sh
\drb-rounder-executable\dist\drb_rounder\drb_rounder.exe <test_filename_here>
```


## Reports Generated
Two log files will be generated in your current working directory (wherever you
are running the executable or python script).

1. `rounder.log` is an application log which is a growing file describing successful runs as well as unsuccessful runs and their errors

2. `rounded_values.log` is a log file which reports what values have been rounded and the values they were rounded to on the previous run of the rounder


## Additional documentation

You will find additional documentation in the (doc/)[doc/] directory and within the source code.

