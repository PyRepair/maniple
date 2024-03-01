### Bug Explanation
The bug in the `table_exists` function arises from the check for the existence of the table in the output of the `run_hive_cmd` function. The function checks if the table name is present in the `stdout` variable, but it does not handle cases where the table name might be a substring within another table name. This leads to incorrect results in certain scenarios.

### Bug Fix Strategy
To fix the bug, we should ensure that the function checks for the exact match of the table name in the `stdout` variable. This will prevent false positives where a substring of the table name matches another table.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By splitting the `stdout` variable using `stdout.split('\n')`, we can ensure that we are checking for an exact match of the table name in the output. This correction addresses the issue of substring matches and should make the function behave correctly in all scenarios.