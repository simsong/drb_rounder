/**************************************************************/
/***                                                        ***/
/***     Rounding Observation Counts          11/1/2017     ***/
/***                                                        ***/
/***  The program rounds the number of observations         ***/
/***  according to the rounding rules as given in the       ***/
/***  RDC DA briefs - rounding document.                    ***/
/***                                                        ***/
/***  To run the code, use the %LET statements to set       ***/
/***  inputfile to be the input file, outputfile to be the  ***/
/***  output file (with the original variables and the      ***/
/***  rounded values) and varlist to be the list of         ***/
/***  variable names to be rounded according to the         ***/
/***  observation count rules, which should be space        ***/
/***  delimited. The output file will include all of the    ***/
/***  original unrounded variables and the rounded          ***/
/***  variables, the latter of which will be denoted by     ***/
/***  appending _r to each variable name.                   ***/
/***                                                        ***/
/***  If inputfile and outputfile are identical, the input  ***/
/***  file will be overwritten.                             ***/
/**************************************************************/

options mprint;

%LET inputfile = dot.descriptive_statistics;
%LET outputfile = dot.descriptive_statistics_roundN;
%LET varlist = samp_size1 samp_size2 samp_size3 samp_size4;

%MACRO round;

data &outputfile;
    set &inputfile;

    %LET i = 1;
    %DO %WHILE ("%SCAN(&varlist.,&i.)" ~= "");
        %LET var = %SCAN(&varlist.,&i.);

        * Round sample sizes/integers to appropriate precision;
        * If an integer is less than 15, the code rounds to 10;
        * But 10 does not actually mean 10; * it means "<15";
        if &var<15 then &var._r=10;
        else if &var<100 then &var._r=round(&var,10);
        else if &var<1000 then &var._r=round(&var,50);
        else if &var<10000 then &var._r=round(&var,100);
        else if &var<100000 then &var._r=round(&var,500);
        else if &var<1000000 then &var._r=round(&var,1000);
	    else &var._r = round(&var.,10**(floor(log10(&var.))-3));

        %LET i = %EVAL(&i.+1);
    %END;
run;

%MEND round;
%round;
