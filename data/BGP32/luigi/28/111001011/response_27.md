### Analysis:
1. The `table_exists` function in the `HiveCommandClient` class checks if a table exists in the specified database, but it does not account for case sensitivity.
2. The issue reported on GitHub points out the case sensitivity problem and suggests checking `stdout` against `table.lower()` to avoid case issues.
3. The function currently checks if the table name is an exact match with the table names returned by Hive, leading to failure due to case inconsistencies.
4. To fix the bug, we need to make the comparison case-insensitive by converting both table name and `stdout` to lowercase before comparison.

### Bug Fix Strategy:
- Convert the `table` parameter to lowercase before using it in the comparison.
- Convert the `stdout` output from the Hive command to lowercase before checking if the table exists.

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

By converting both the table name and the `stdout` output to lowercase in the comparison, the `table_exists` function will now be case-insensitive, as suggested in the GitHub issue.