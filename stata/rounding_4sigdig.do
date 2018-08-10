/**************************************************************/
/***                                                        ***/
/***     Rounding to Four Significant Digits  11/3/2017     ***/
/***                                                        ***/
/***  The program rounds according to the rules as given    ***/
/***  in the RDC DA briefs - rounding document.             ***/
/***                                                        ***/
/***  To run the code, call the do file as follows          ***/
/***                                                        ***/
/***    do rounding_4sigdig var1 var2                       ***/
/***                                                        ***/
/***  where "var1" and "var2" are examples of variable      ***/
/***  names in the data that are to be rounded to four      ***/
/***  significant digits. The program as written will round ***/
/***  up to 9 variables (this can be easily enlarged by     ***/
/***  lengthening the foreach statement).                   ***/
/***                                                        ***/
/**************************************************************/

foreach var in "`1'" "`2'" "`3'" "`4'" "`5'" "`6'" "`7'" "`8'" "`9'" {
if "`var'"=="" exit

replace `var' = round(`var',10^(floor(log10(abs(`var')))-3))

}


