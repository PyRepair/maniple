The bug in the provided function is that the condition checking for the presence of the table in the stdout is incorrect, leading to incorrect return values.

### Bug Cause:
- In the first case (where partition is None), the function checks if the table name is present in the stdout output of the 'show tables like' command to determine if the table exists. This check is incorrect as 'show tables like' may return other tables with similar names as well, resulting in a false positive.

- In the second case (where partition is not None), the function checks if the stdout exists to determine if the table exists. This is also incorrect as the stdout may contain other information leading to incorrect results.

### Strategy for Fixing the Bug:
- For both cases, the function should explicitly check if the exact table name is present in the output of the 'show tables' command to determine if the table exists. This will ensure that only the exact table name is considered for existence.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))

        return stdout and table in stdout.split()
    else:
        stdout = run_hive_cmd("""use {0}; show tables like '{1}';""".format(database, table))

        return stdout and table in stdout
```

This corrected function explicitly checks for the exact table name in the output of the 'show tables' command, ensuring accurate detection of table existence.