### Bug Analysis:
The bug in the `table_exists` function arises from the condition checks on the `stdout` variable. In the first case, the return value is checked against `stdout and table in stdout`, which evaluates to `True` only if `stdout` is not empty and `table` is found in `stdout`. However, in the second case, the return value is simply checked against the existence of `stdout`, resulting in different behavior for checking table existence.

The bug causes the function to return incorrect values, specifically failing to identify the presence of tables when the output contains the table name due to inconsistent condition checks.

### Bug Fix Strategy:
To fix the bug, we should modify the condition check on the `stdout` variable to ensure consistent behavior for both cases. By explicitly checking for the presence of the table name in the `stdout`, we can accurately determine if the table exists.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout.split("\n")
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By modifying the return value to explicitly check for the table name in the `stdout` and adjusting the condition check in the second case to return `bool(stdout)`, the corrected function should now accurately determine if a table exists in a Hive database.