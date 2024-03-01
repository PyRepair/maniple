The bug in the `table_exists` function is related to the case sensitivity of the comparison between the table name and the table name extracted from `stdout`. When the table name is provided with different cases, the comparison fails leading to incorrect results.

### Bug Cause:
The bug occurs because the function does not perform a case-insensitive comparison. The `table in stdout` or `table == stdout` comparisons are case-sensitive, leading to failures when the case of the table name does not match that in `stdout`.

### Fix Strategy:
To fix the bug, we need to convert both the table name and the value extracted from `stdout` to lowercase before comparing them. This change will make the comparison case-insensitive, allowing the function to work correctly irrespective of the case of the table names.

### Corrected Version:
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

By making this change, the function will perform a case-insensitive comparison, resolving the bug reported in the GitHub issues.