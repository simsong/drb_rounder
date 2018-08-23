/*********************************************************************
Rounds every number in file according to RDC rounding rules for counts.

Comma is a delimiter, so if you have numbers like 1,000,000 in you 
original text file, then you should search-and-replace before
running this code.
*********************************************************************/

%let mydir=;
%let infile=;
%let delimiter_list=" ","	","|","-",",",";",":","(",")","<",">","'",'"';

*** First grab maximum record length;
data _null_;
  infile "&mydir./&infile." end=lastrecord;
  input;
  retain max_length 0;
  max_length=max(max_length,length(_infile_));
  if lastrecord then do;
    call symput("max_length",compress(put(max_length,12.)));
    call symput("max_new_length",compress(put(1.5*max_length,12.)));
  end;
run;
filename outfile "&mydir./round_&infile.";
*** Now go through file, identify numbers, round if necessary, and replace;
data _null_;
  length temp $&max_length..;
  length newline new_part $&max_new_length..;
  length cur_char prev_char1 prev_char2 $1.;
  infile "&mydir./&infile." _infile_=original length=rec_length;
  input;
  /*** Only search for numbers if there actually is a record of any length ***/
  if rec_length>0 then do;
    /*** initialize some variables before the search ***/
    newline=repeat(" ",&max_new_length.-1); found_number=0; prev_char1=""; prev_char2=""; extra_spaces=0; first_char=.;
    file LOG;
    put original;
    /*** Search, character by character for numbers ***/
    do i=1 to rec_length;
      cur_char=substr(original,i,1);
      if first_char=. and cur_char ne " " then first_char=i;
      if found_number=0 then do;
        if cur_char in ("0","1","2","3","4","5","6","7","8","9") then do;
          /*** OK, found a number -- what preceded it? If period, then this might be a decimal ***/
          if prev_char1="." then check_delim=prev_char2; else check_delim=prev_char1;
          /*** Might need to edit this depending on what characters might serve as delimiters -- currently space, tab, negative sign, and pipe ***/
          if check_delim in (&delimiter_list.) or i=1 or (prev_char1="." and i=2) then do;
            /*** if this is potentially the start of a number, set found_number to 1 and start storing numeric string ***/
            temp_start=i;
            found_number=1;
            num_dots=0;
            temp=cur_char;
            round_flag=1;
            num_chars=1;
            num_digits=1;
            if prev_char1="." then do;
              temp_start=i-1;
              num_dots=1;
              temp=prev_char1 || cur_char;
              num_chars=2;
            end;
            if i=rec_length then substr(newline,i+extra_spaces,1)=cur_char;
          end;
          /*** if the previous character was not a delimiter and we are not in the midst
          of a potential numeric string, then update string and continue with search ***/
          else substr(newline,i+extra_spaces,1)=cur_char;
        end;
        /*** non-numeric character so update string and continue with search ***/
        else substr(newline,i+extra_spaces,1)=cur_char;
      end;
      else do;
        /*** since found_number=1, we are potentially in the midst of a numeric string ***/
        if num_dots=0 then do;
          if cur_char in (".","0","1","2","3","4","5","6","7","8","9") then do;
            /*** still potentially a number ***/
            temp=trim(temp) || cur_char;
            num_chars=num_chars+1;
            if cur_char="." then num_dots=1;
            else num_digits=num_digits+1;
          end;
          else if cur_char in (&delimiter_list.) then found_number=0;
          else do;
            found_number=0;
            round_flag=0;
          end;
        end;
        else do;
          if cur_char in (".","0","1","2","3","4","5","6","7","8","9") then do;
            temp=trim(temp) || cur_char;
            num_chars=num_chars+1;
            if cur_char="." then round_flag=0; /*** two periods found in numeric string so this is not a regular number -- might be a version number, eg 1.0.1 ***/
            else num_digits=num_digits+1;
          end;
          else if cur_char in (&delimiter_list.) then found_number=0;
          else do;
            /*** Digits immediately followed by a non-delimiting character indicate that this is not really a statistic, eg 09875BCQ21 ***/
            found_number=0;
            round_flag=0;
          end;
        end;
        if found_number=0 or i=rec_length then do;
          /*** We have reached the end of a numeric string -- does it need rounding? ***/
          if round_flag=1 then do;
            tmp=int(input(temp,12.));
            if tmp<15 then tmp=15;
            else if tmp<100 then tmp=round(tmp,10);
            else if tmp<1000 then tmp=0.5*round(2*tmp,100);
            else if tmp<10000 then tmp=round(tmp,100);
            else if tmp<100000 then tmp=0.5*round(2*tmp,1000);
            else if tmp<1000000 then tmp=round(tmp,1000);
            else tmp=round(tmp,10**(int(log10(tmp))-3));
            /*** replace original numeric string with rounded string and adjust as needed to fill the same column space in record ***/
            new_part=compress(put(tmp,12.));
            new_length=length(compress(new_part));
            if new_length<num_chars then do;
              substr(newline,temp_start+extra_spaces,num_chars-new_length)=repeat(" ",(num_chars-new_length)-1);
              substr(newline,temp_start+extra_spaces+(num_chars-new_length),new_length)=compress(new_part);
            end;
            else if new_length>num_chars then do;
              substr(newline,temp_start+extra_spaces,new_length)=new_part;
              extra_spaces=extra_spaces+(new_length-num_chars);
            end;
            else substr(newline,temp_start+extra_spaces,num_chars)=new_part;
            if i<rec_length then substr(newline,i+extra_spaces,1)=cur_char;
          end;
          else do;
            /*** no rounding needed, so output original numeric string ***/
            substr(newline,temp_start+extra_spaces,num_chars)=temp;
            substr(newline,i+extra_spaces,1)=cur_char;
          end;
        end;
      end;
      prev_char2=prev_char1;
      prev_char1=cur_char;
    end;
    put newline;
    file outfile;
    if first_char>1 then put + (first_char-1) newline;
    else put newline;
  end;
  else do;
    /*** if empty record, maintain that in new file ***/
    put original;
    file outfile;
    put original;
  end;
run;






