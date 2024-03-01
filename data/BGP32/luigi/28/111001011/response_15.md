The bug in the `table_exists` function arises from case sensitivity when comparing the table name in stdout with the provided table name. The function needs to be modified to handle case-insensitive comparisons to resolve the issue mentioned in the GitHub post.

### Bug Cause:
The function currently checks if the `table` string is exactly present in the `stdout` string received from the `run_hive_cmd` function, which leads to case-sensitive mismatches.

### Bug Fix Strategy:
Modify the comparison to be case-insensitive by converting both the `table` and `stdout` strings to lowercase before comparison.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By making the comparison case-insensitive in the corrected function version, the issue described in the GitHub post should be resolved. Now, the `table_exists` function will accurately detect the table's existence regardless of case differences.