import helpers
from helpers import LESS_THAN_15, ROUND4_METHOD, COUNTS_METHOD

class Number:
    """
    This class represents any number that is going to be evaluated by the DRB
    Rounder. The class maintains properties of the number and rounds the number
    based on respective rounding policies.
    """

    def __init__(self, orig, method=None):
        """
        Initialize all the variables that need to be maintained for numbers
        """
        self.original = str(orig)
        self.original_cleaned = None
        self.rounded_cleaned = None
        self.rounded = None
        self.leading_text = None
        self.trailing_text = None
        self.has_commas = None
        self.in_scientific_form = None
        self.method = method
        self.needed_rounding = None

    def __repr__(self):
        return "<Number:"+self.original+">"

    def init_for_testing(self, rounding_info):
        self.original = rounding_info['original']
        self.original_cleaned = rounding_info['original_cleaned']
        self.rounded_cleaned = rounding_info['rounded_cleaned']
        self.rounded = rounding_info['rounded']
        self.leading_text = rounding_info['leading_text']
        self.trailing_text = rounding_info['trailing_text']
        self.has_commas = rounding_info['has_commas']
        self.in_scientific_form = rounding_info['in_scientific_form']
        self.method = rounding_info['method']
        self.needed_rounding = rounding_info['needed_rounding']

    def clean(self):
        """
        This function cleans the original value to prepare it for rounding

        Note: if there are non-digit characters sandwiched between digit
        characters, the non-digit characters will not be removed
        """
        val = str(self.original)

        # Remove leading non-digits
        digit_chars   = "0123456789."
        leading_text  = ""
        trailing_text = ""
        while len(val)>0 and val[0] not in digit_chars:
            leading_text = leading_text + val[0]
            val = val[1:]

        # Return if the removal of non-digits results in an empty string
        if val == "":
            self.original_cleaned = ""
            self.leading_text = leading_text
            self.trailing_text = trailing_text
        else:
            # Remove trailing non-digits
            while len(val)>0 and val[-1] not in digit_chars:
                trailing_text = val[-1] + trailing_text
                val = val[:-1]

        # Check to see if there are commas
        self.has_commas = "," in val

        # Remove commas
        val = val.replace(",", "")

        # Is the value in scientific form?
        self.in_scientific_form = helpers.in_scientific_form(val)

        # If it's in scientific form, remove scientific notation
        if self.in_scientific_form:
            if "." in val:
                val = str(float(val))
            else:
                val = str(int(float(val)))

        self.original_cleaned = val
        self.leading_text = leading_text
        self.trailing_text = trailing_text
        return

    def reconstruct(self):
        """
        This function rebuilds the rounded value to resemble the original string
        """
        ret = ""  # Rounded value being reconstructed

        # Put back into scientific form
        if self.in_scientific_form:
            x = '%E' % float(self.rounded_cleaned)
            self.rounded_cleaned = x.split('E')[0].rstrip('0').rstrip('.') + 'E' + x.split('E')[1]

        # Add commas back to original string if they were initially there
        if self.rounded_cleaned == LESS_THAN_15:
            ret = self.rounded_cleaned
        elif "," in self.original and self.method == COUNTS_METHOD:
            ret = "{:,}".format(int(self.rounded_cleaned))
        elif "," in self.original and self.method == ROUND4_METHOD:
            ret = "{:,}".format(float(self.rounded_cleaned))
        else:
            ret = "{:}".format(self.rounded_cleaned)

        # Put full string back together
        ret = self.leading_text + ret + self.trailing_text

        # Add spaces back in
        ret += " " * (len(self.original) - len(ret))
        assert len(self.original) <= len(ret)  # when "1" converts to "<15" or "1234." to "1234.0"

        self.rounded = ret
        return

    def round(self):
        """
        Rounds the string based on respective rounding rules
        """
        import re

        # Cleans string / records original_cleaned, leading_text, trailing_text, and has_commas
        self.clean()

        # Don't round if:
        #   - the value is not in scientific form and also follows a constraint below
        #   - there are alphabetical letters in the original string
        #   - the cleaned string is an empty string
        #   - there are still other symbols found in the cleaned string
        if not self.in_scientific_form:
            self.needed_rounding = False
            if re.search('[a-zA-Z]', self.original) : return
            if self.original_cleaned == "" : return
            if re.search("\\D", self.original_cleaned.replace(".", "")) : return

        # Perform the appropriate method of rounding.
        self.needed_rounding = True
        total_digits = helpers.find_sigfigs(self.original_cleaned) + helpers.num_trailing_zeros(self.original_cleaned)

        if ("." in self.original_cleaned) or (self.method==ROUND4_METHOD):  # pylint: disable=E1135
            self.method = ROUND4_METHOD
            self.rounded_cleaned = str(helpers.round4_float(float(self.original_cleaned)))
            if total_digits > 4:
                self.rounded_cleaned = helpers.remove_trailing_zero(self.rounded_cleaned)
        else:
            self.method = COUNTS_METHOD
            self.rounded_cleaned = str(helpers.round_counts(self.original_cleaned))

        # Reconstruct the rounded string
        self.reconstruct()

        # Was rounding really needed?
        if self.rounded_cleaned == LESS_THAN_15:
            self.needed_rounding = True
        elif self.method == ROUND4_METHOD and self.in_scientific_form:
            self.needed_rounding = float(self.original_cleaned) != float(self.rounded_cleaned)
        elif self.method == ROUND4_METHOD and total_digits <= 4:
            self.needed_rounding = float(self.original_cleaned) != float(self.rounded_cleaned)
        else:
            self.needed_rounding = self.original != self.rounded

        return self.rounded
