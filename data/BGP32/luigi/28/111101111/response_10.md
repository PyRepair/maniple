The bug in the `table_exists` function is that it does a case-sensitive check for the table name present in the output of the `run_hive_cmd` function. To fix this bug, we need to convert both the table name and the stdout to lowercase before comparing them.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd(f"use {database}; show partitions {table} PARTITION ({self.partition_spec(partition)})")

        return bool(stdout)
```

By converting both the table name and the stdout to lowercase before comparison, the function will now be case insensitive, fixing the bug reported in the GitHub issue #896.