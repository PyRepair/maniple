### Bug Explanation
The bug in the `copy` function lies in the construction of the `colnames` variable. If the `self.columns` attribute is `None`, the code does not handle this case properly and attempts to iterate over it to construct the `colnames` string. This leads to an error when trying to join the elements of a `None` object.

### Bug Fix Strategy
To fix the bug, we need to check if `self.columns` is `None` before constructing the `colnames` string. If it is `None`, then `colnames` should be an empty string.

### Corrected Function
```python
def copy(self, cursor, f):
    """
    Defines copying from s3 into redshift.

    If both key-based and role-based credentials are provided, role-based will be used.
    """
    logger.info("Inserting file: %s", f)
    colnames = ''
    if self.columns is not None and len(self.columns) > 0:
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

After applying this correction, the function should now properly handle cases where `self.columns` is `None`, ensuring that the `colnames` variable is set to an empty string in such situations.