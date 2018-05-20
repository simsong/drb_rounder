/**************************************************************/
/***                                                        ***/
/***     Rounding Observation Counts          11/3/2017     ***/
/***                                                        ***/
/***  The program rounds the number of observations         ***/
/***  according to the rounding rules as given in the       ***/
/***  RDC DA briefs - rounding document.                    ***/
/***                                                        ***/
/***  To run the code, call the do file as follows          ***/
/***                                                        ***/
/***    do rounding_N.do N dof                              ***/
/***                                                        ***/
/***  where "N" and "dof" are examples of variable names    ***/
/***  in the data that are to be rounded according to       ***/
/***  the observation count rules. The program as written   ***/
/***  will round up to 9 variables (this can be easily      ***/
/***  enlarged by lengthening the foreach statement).       ***/
/***                                                        ***/
/**************************************************************/

foreach var in "`1'" "`2'" "`3'" "`4'" "`5'" "`6'" "`7'" "`8'" "`9'" {
if "`var'"=="" exit

replace `var' = round(`var', 10) if `var'>=15&`var'<=99 
replace `var' = round(`var', 50) if `var'>=100&`var'<=999 
replace `var' = round(`var', 100) if `var'>=1000&`var'<=9999 
replace `var' = round(`var', 500) if `var'>=10000&`var'<=99999 
replace `var' = round(`var', 1000) if `var'>=100000&`var'<=999999 
replace `var' = round(`var',10^(floor(log10(`var'))-3)) if `var'>=1000000 

if `var'<15 capture gen `var'_less15=0
capture replace `var'_less15=1 if `var'<15
capture replace `var'_less15=0 if `var'>=15
replace `var'=. if `var'<15
}


