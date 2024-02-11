The error message originates from a failing test for a pivot_table function, which is written for a DataFrame in a pandas library.

An AttributeError is being raised due to a 'Series' object's columns being accessed, which does not actually have the 'columns' attribute.

The source of the error comes from the problematic section of the input DataFrame passed to the pivot_table function. It arises due to attempting to access the columns attribute of the 'Series' object passed as the column argument, which is the root cause of the failure in all test cases.

The input variable 'cols' sets a MultiIndex for the columns of the DataFrame inside the pivot_table function, causing an error when making attribute references to a Series object.

Simplified error message:
"AttributeError: 'Series' object has no attribute 'columns'."