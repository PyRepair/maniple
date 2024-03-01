### Analysis:
- The bug occurs in the `copy` function of the `S3CopyToTable` class in the `luigi.contrib.redshift.py` file.
- The error happens when trying to check the length of `self.columns` which is set to `None`.
- The error message indicates a `TypeError: object of type 'NoneType' has no len()`.
- The expected behavior is to handle the case where `self.columns` is `None` gracefully without throwing an error.

### Bug Cause:
- The bug is caused by trying to get the length of `self.columns` without checking if it is `None`.

### Bug Fix:
To fix the bug, we need to first check if `self.columns` is `None` before trying to get its length. If `self.columns` is `None`, we can set `colnames` to an empty string.

### Corrected Version:
```python
def copy(self, cursor, f):
    """
    Defines copying from s3 into redshift.

    If both key-based and role-based credentials are provided, role-based will be used.
    """
    logger.info("Inserting file: %s", f)
    colnames = ''
    if self.columns is not None:
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

After making the above changes, the `copy` function will handle the case where `self.columns` is `None` and prevent the `TypeError` from occurring.