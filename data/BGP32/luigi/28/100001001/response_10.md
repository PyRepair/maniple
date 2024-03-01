### Bug Explanation
The bug in the `table_exists` function is that it checks if the `table` string is present in the `stdout` string without considering case sensitivity. This leads to incorrect results when comparing table names due to differences in the case of characters in the strings.

### Bug Fix
To fix the bug, we need to make the comparison case-insensitive by converting both the `table` and `stdout` strings to lowercase before checking for existence. This ensures that the comparison is not affected by differences in character case.

### Corrected Version
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