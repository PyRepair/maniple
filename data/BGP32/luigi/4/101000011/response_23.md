## Analysis:
The bug occurs in the `copy` function of the `S3CopyToTable` class in the `luigi/contrib/redshift.py` file. The bug arises when the `self.columns` is `None`, causing a `TypeError` when trying to get the length of `None`.

## Error Location:
The error occurs in this line:
```python
if len(self.columns) > 0:
```
When `self.columns` is `None`, it throws a `TypeError` because `None` has no length.

## Cause of the Bug:
The bug is caused by not handling the case when `self.columns` is `None` properly. The `copy` function assumes that `self.columns` will always have a value and tries to access its length without checking if it is `None`.

## Bug Fix Strategy:
To fix the bug, we need to check if `self.columns` is not `None` before trying to get its length. If `self.columns` is `None`, we should handle this case appropriately without attempting to access its length.

## Corrected Version:
Here is the corrected version of the `copy` function:

```python
def copy(self, cursor, f):
    """
    Defines copying from s3 into redshift.

    If both key-based and role-based credentials are provided, role-based will be used.
    """
    logger.info("Inserting file: %s", f)
    colnames = ''
    
    if self.columns and len(self.columns) > 0:
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

In the corrected version, we first check if `self.columns` is not `None` before attempting to get its length. This change will prevent the `TypeError` when `self.columns` is `None`, resolving the issue reported on GitHub.