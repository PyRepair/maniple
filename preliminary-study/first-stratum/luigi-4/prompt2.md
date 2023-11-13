Fact used: f1-1-1, f2-2-1

# Prompt
Please fix the code provided below and provide the corrected code as the output.
The buggy source code is:

```python
def copy(self, cursor, f):
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

The error message is:

```python
self = <contrib.redshift_test.TestS3CopyToTable testMethod=test_s3_copy_with_nonetype_columns>
mock_redshift_target = <MagicMock name='RedshiftTarget' id='139768575303008'>

    @mock.patch("luigi.contrib.redshift.RedshiftTarget")
    def test_s3_copy_with_nonetype_columns(self, mock_redshift_target):
        task = DummyS3CopyToTableKey(columns=None)
>       task.run()

test/contrib/redshift_test.py:337: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
luigi/contrib/redshift.py:338: in run
    self.copy(cursor, path)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = DummyS3CopyToTableKey(table=dummy_table, columns=null)
cursor = <MagicMock name='RedshiftTarget().connect().cursor()' id='139768574974560'>
f = 's3://bucket/key'

    def copy(self, cursor, f):
        """
        Defines copying from s3 into redshift.
    
        If both key-based and role-based credentials are provided, role-based will be used.
        """
        logger.info("Inserting file: %s", f)
        colnames = ''
>       if len(self.columns) > 0:
E       TypeError: object of type 'NoneType' has no len()

luigi/contrib/redshift.py:356: TypeError
```


# Response
The issue with the code is that it does not handle the case when `self.columns` is `None`. To fix this, we can add a check for `None` before checking its length and set `colnames` accordingly.

Here's the corrected code:

```python
def copy(self, cursor, f):
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

With this change, the code will first check if `self.columns` is not `None` before trying to get its length, and set `colnames` accordingly. This should resolve the issue encountered in the test.

