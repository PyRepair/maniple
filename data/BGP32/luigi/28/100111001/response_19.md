### Bug Explanation
The bug in the `table_exists` function lies in the conditional checks for whether a table exists. The function incorrectly checks if the table name is present in the `stdout` variable, which may include additional content besides just the table name. This leads to incorrect evaluation of whether the table exists or not.

### Bug Fix Strategy
To fix the bug, we need to modify the conditional checks to correctly determine if the table name exists in the output obtained from the `run_hive_cmd` function.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')  # Modify the check to split the stdout and verify against individual lines
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)  # Simplify the return statement to check if stdout is non-empty
```

By splitting the `stdout` output and checking each line individually in the first case, and simplifying the conditional check in the second case, the corrected function should now properly determine if a table exists in the given database. This should address the failing tests and resolve the bug.