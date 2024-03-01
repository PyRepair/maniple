### Bug Explanation
The bug in the `copy` function is caused by the incorrect formatting of the `COPY` query string. The `colnames` variable is being formatted with parentheses even when there are no columns specified, leading to a syntax error in the SQL query.

### Bug Fix Strategy
To fix the bug, we need to only add parentheses to `colnames` if there are actually columns specified. If there are no columns, `colnames` should remain an empty string.

### Corrected Version
```python
def copy(self, cursor, f):
    """
    Defines copying from s3 into redshift.

    If both key-based and role-based credentials are provided, role-based will be used.
    """
    logger.info("Inserting file: %s", f)
    colnames = ''
    if self.columns:
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

Now, the `colnames` variable will only be surrounded by parentheses if there are actual columns specified, otherwise it will remain an empty string. This will prevent the SQL syntax error when executing the `COPY` query.