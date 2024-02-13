You have been provided with a description for GitHub issue. However, it may be ambiguous, please simplify it and make it readable by developer while keeping the key information.

Here is an example summary of a GitHub issue:

GitHub Bug Title:
TypeError when calling mean on a DataFrameGroupBy with Int64 dtype

Description:
Using the new nullable integer data type, calling mean after grouping results in a TypeError. It works with int64 dtype and also with Int64 dtype when taking a single column to give a SeriesGroupBy. The error occurs with median and std as well. However, it does not occur with min, max, or first.

Expected Output:
When performing aggregation operations on a DataFrameGroupBy object with columns of nullable integer data type (Int64), the following behaviours are expected for the specified methods:
mean(): The method should compute the mean of grouped data without raising a TypeError.
median():The method should compute the median of grouped data without raising a TypeError.
std(): The method should compute the standard deviation of grouped data without raising a TypeError.

Environment:
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0


# The source code of the buggy function
```python
# The relative path of the buggy file: luigi/contrib/redshift.py



    # this is the buggy function you need to fix
    def copy(self, cursor, f):
        """
        Defines copying from s3 into redshift.
    
        If both key-based and role-based credentials are provided, role-based will be used.
        """
        logger.info("Inserting file: %s", f)
        colnames = ''
        if len(self.columns) > 0:
            colnames = ",".join([x[0] for x in self.columns])
            colnames = '({})'.format(colnames)
    
        cursor.execute("""
         COPY {table} {colnames} from '{source}'
         CREDENTIALS '{creds}'
         {options}
         ;""".format(
            table=self.table,
            colnames=colnames,
            source=f,
            creds=self._credentials(),
            options=self.copy_options)
        )
    
```


# A GitHub issue title for this bug
```text
Redshift COPY fails in luigi 2.7.1 when columns are not provided
```

## The GitHub issue's detailed description
```text
Running Redshift COPY jobs with columns = None to prohibit table creation fails in luigi 2.7.1 with

TypeError: object of type 'NoneType' has no len()
The root cause seems to be https://github.com/spotify/luigi/pull/2245/files#diff-778ea3db4cccaf4de6564889c5eb670fR338

A possible solution would be to change the line to

if self.columns and len(self.columns) > 0:
unless I am missing some reason to explicitly ask only for len(self.columns).
```