### Analysis
The buggy function `table_exists` is designed to check whether a table exists in a given database. It uses the `run_hive_cmd` function to execute Hive queries and determine the existence of the table. The bug seems to be related to the handling of the output `stdout` from the `run_hive_cmd` function.

### Issues
1. In the first case, even though the table exists (as indicated by the 'OK' in stdout), the function fails to return `True`.
2. In the second case, the table exists in the stdout output, but due to case sensitivity with 'MyTable' in the stdout and 'mytable' in the query, the function fails to return `True`.

### Bug Cause
The bug is caused by the `table in stdout` check in the first case, which is case-sensitive. In Hive, the table names are case-insensitive, leading to discrepancies in the comparison.

### Fix Strategy
1. Normalize the table name comparisons to make them case-insensitive by converting both the table name and the content from `stdout` to lowercase for comparison.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

Now, the function will first convert both the table name (`table`) and the content from `stdout` to lowercase before comparison, making the check case-insensitive.