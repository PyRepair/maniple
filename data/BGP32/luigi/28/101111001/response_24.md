### Bug Explanation
The bug in the `table_exists` function lies in the way the function checks for the existence of a table in the given database. The function currently checks for the presence of the table name in the output of the `run_hive_cmd` function. However, the function does not correctly handle cases where the table name is a substring of another table name in the output, leading to incorrect results.

### Bug Fix Strategy
To fix the bug, we need to modify the conditional check in the `table_exists` function to ensure that it correctly matches the table names in the output of the `run_hive_cmd` function. This can be achieved by splitting the output of `run_hive_cmd` by newline characters and then checking for an exact match with the table name.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By splitting the `stdout` by newline characters and checking for an exact match with the table name, we ensure that the function correctly identifies the existence of the table even if it is a substring of another table name.