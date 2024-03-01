### Bug Explanation
The bug in the `table_exists` function is due to the inconsistent handling of the returned `stdout` variable. In the first branch of the `if` statement, the function checks if the table name is present in the entire stdout string. In the second branch, the function simply checks if `stdout` exists. This inconsistency leads to incorrect results.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function always checks for the full table name match in the entire `stdout` string. This can be achieved by modifying the condition in the second branch of the `if` statement.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout and table in stdout
```

By making sure to check for the table name within the entire `stdout` string in both branches of the `if` statement, the corrected version of the function should now pass the failing test cases.