### Bug Explanation:
The bug in the `table_exists` function is due to a case sensitivity mismatch when checking if a table exists in the Hive database. The function compares the table name directly with the output from running a Hive command, leading to failures when the case of the table name does not match the case in the Hive metadata.

### Solution Strategy:
To fix the bug and make the `table_exists` function case insensitive, we need to convert both the table name and the output from the Hive command to lowercase before comparing them.

### Corrected Version of the Function:
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

### Explanation:
- In the corrected version, both the `table` and the `stdout` values are converted to lowercase using the `lower()` method before comparison.
- This modification ensures a case-insensitive check for the presence of the table in the Hive metadata.
- The return statement for the function is simplified to directly return the boolean result of `stdout`, eliminating the need for an explicit conditional check.