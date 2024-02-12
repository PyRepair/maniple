The original error message reads: "TypeError: object of type 'NoneType' has no len()" 

The error occurred in the 'copy' function at line 356 in 'luigi/contrib/redshift.py'. 
The failing test method 'test_s3_copy_with_nonetype_columns' called the 'run' method of 'DummyS3CopyToTableKey', which in turn called the 'copy' method passing a 'None' value for the 'columns' parameter. This caused a 'TypeError' because the 'len' method cannot be used on a 'NoneType' object.

Simplified Error: "TypeError: object of type 'NoneType' has no len()" occurred in 'luigi/contrib/redshift.py' at line 356 while calling 'copy' method from the 'DummyS3CopyToTableKey' which passed a 'None' value.