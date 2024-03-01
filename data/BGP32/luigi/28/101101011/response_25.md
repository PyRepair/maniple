### Identified Bug:
The bug in the `table_exists` function is that it is not performing a case-insensitive check when comparing the table name with the output received from the `run_hive_cmd` function.

### Cause of the Bug:
The buggy function `table_exists` is comparing the `table` parameter with the `stdout` output without converting them to a common case, causing case-sensitive comparison issues. This is evident from the failing test cases where the table name in the `stdout` is in lower case, but the comparison is against the original table name provided.

### Fix Strategy:
To fix the bug, convert both the `table` parameter and the `stdout` output to a common case (lower or upper) for a case-insensitive comparison.

### Corrected Version of the `table_exists` function:
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

By converting both `table` and `stdout` to lowercase before comparison, the corrected version of the function ensures a case-insensitive check for table existence. This correction aligns with the suggested fix in GitHub issue #896, addressing the case sensitivity problem.