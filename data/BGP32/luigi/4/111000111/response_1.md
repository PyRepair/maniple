### Analysis:
1. The `copy` function in the `S3CopyToTable` class is responsible for copying data from S3 into Redshift.
2. The bug occurs when `self.columns` is `None`, leading to a `TypeError` due to trying to get the length of `None`.
3. The `copy` function constructs a SQL query for `COPY` command but doesn't handle the case when `self.columns` is `None` correctly.
4. We need to modify the condition where the `len(self.columns) > 0` check is performed to handle the case when `self.columns` is `None`.

### Bug Fixing Strategy:
1. Update the condition to check if `self.columns` is not `None` and then proceed to construct the `colnames` string.
2. When `self.columns` is `None`, `colnames` will be an empty string.
3. This will prevent the `TypeError` when trying to get the length of `None`.

### Corrected Version:
```python
# The relative path of the corrected file: luigi/contrib/redshift.py

class S3CopyToTable(rdbms.CopyToTable, _CredentialsMixin):
    ...

    def copy(self, cursor, f):
        """
        Defines copying from s3 into redshift.
    
        If both key-based and role-based credentials are provided, role-based will be used.
        """
        logger.info("Inserting file: %s", f)
        colnames = ''
        if self.columns and len(self.columns) > 0:  # Updated condition to handle NoneType
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
            options=self.copy_options())
        )  # Modified to call copy_options as a function
```

By making the above changes, the bug causing a `TypeError` when `self.columns` is `None` should be resolved, and the function should work as expected.