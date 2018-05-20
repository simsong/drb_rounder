/**************************************************************/
/***                                                        ***/
/***     Rounding to Four Significant Digits  11/1/2017     ***/
/***                                                        ***/
/***  The program rounds according to the rules as given    ***/
/***  in the RDC DA briefs - rounding document.             ***/
/***                                                        ***/
/***  To run the code, use the %LET statements to set       ***/
/***  inputfile to be the input file, outputfile to be the  ***/
/***  output file (with the original variables and the      ***/
/***  rounded values) and varlist to be the list of         ***/
/***  variable names to be rounded to four significant      ***/
/***  digits, which should be space delimited. The output   ***/
/***  file will include all of the original unrounded       ***/
/***  variables and the rounded variables, the latter of    ***/
/***  which will be denoted by appending _4 to each         ***/
/***  variable name.                                        ***/
/***                                                        ***/
/***  If inputfile and outputfile are identical, the input  ***/
/***  file will be overwritten.                             ***/
/**************************************************************/

%LET inputfile = dot.descriptive_statistics;
%LET outputfile = dot.descriptive_statistics_round4;
%LET varlist = var1 var2 var3;

options mprint;

%MACRO round;

data &outputfile;
    set &inputfile;

    %LET i= 1;
	* Scan varlist for variable names;
	%DO %WHILE ("%SCAN(&varlist.,&i.)" ~= "");
        %LET var = %SCAN(&varlist.,&i.);

		* Round to four significant digits;
		&var._4 = round(&var.,10**(floor(log10(&var.))-3));

        %LET i = %EVAL(&i.+1);
    %END;
run;

%MEND round;
%round;
