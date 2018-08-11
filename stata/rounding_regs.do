/**************************************************************/
/***                                                        ***/
/***     Post Regression Rounding             9/7/2017      ***/
/***                                                        ***/
/***  The program rounds the coefficients and observation   ***/
/***  counts after a regression. The program modifies the   ***/
/***  post estimation scalars and coefficient matrix in     ***/
/***  anticiption of additonal postestimation commands      ***/
/***  such as estout and outreg.                            ***/
/***                                                        ***/
/**************************************************************/

capture program drop round
program define round, eclass
   mat A = e(b)
   forval j = 1/`=colsof(matrix(A))' { 
      mat A[1,`j'] = round(A[1,`j'],10^(floor(log10(abs(A[1,`j'])))-3))
   } 
   ereturn repost b = A

   if e(N)>=15&e(N)<=99 ereturn scalar N = round(e(N), 10)
   if e(N)>=100&e(N)<=999 ereturn scalar N = round(e(N), 50)
   if e(N)>=1000&e(N)<=9999 ereturn scalar N = round(e(N), 100)
   if e(N)>=10000&e(N)<=99999 ereturn scalar N = round(e(N), 500)
   if e(N)>=100000&e(N)<=999999 ereturn scalar N = round(e(N), 1000)
   if e(N)=>1000000 ereturn scalar N = round(e(N),10^(floor(log10(e(N)))-3))

   if e(N)<15 {
   scalar N_less15=1
   ereturn scalar N=.
   }

   if e(df_r)>=15&e(df_r)<=99 ereturn scalar df_r = round(e(df_r), 10)
   if e(df_r)>=100&e(df_r)<=999 ereturn scalar df_r = round(e(df_r), 50)
   if e(df_r)>=1000&e(df_r)<=9999 ereturn scalar df_r = round(e(df_r), 100)
   if e(df_r)>=10000&e(df_r)<=99999 ereturn scalar df_r = round(e(df_r), 500)
   if e(df_r)>=100000&e(df_r)<=999999 ereturn scalar df_r = round(e(df_r), 1000)
   if e(df_r)=>1000000 ereturn scalar df_r = round(e(df_r),10^(floor(log10(e(df_r)))-3))

   if e(df_r)<15 {
   scalar df_less15=1
   ereturn scalar df_r=.
   }


   capture ereturn scalar r2 = round(e(r2),10^(floor(log10(e(r2)))-3))
   capture ereturn scalar r2_a = round(e(r2_a),10^(floor(log10(e(r2_a)))-3))
   capture ereturn scalar F = round(e(F),10^(floor(log10(e(F)))-3))
   capture ereturn scalar rmse = round(e(rmse),10^(floor(log10(e(rmse)))-3))
   capture ereturn scalar mss = round(e(mss),10^(floor(log10(e(mss)))-3))
   capture ereturn scalar rss = round(e(rss),10^(floor(log10(e(rss)))-3))

end

round



