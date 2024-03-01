### Bug Explanation
The bug in the `table_exists` function arises from how the function checks for the existence of a table based on the output of the `run_hive_cmd` function. The function is currently checking if the table name is in the `stdout` string returned by `run_hive_cmd`. This check is insufficient because the `stdout` could contain multiple lines if there are multiple tables matching the pattern.

### Bug Fix Strategy
To fix the bug, we need to modify the check to ensure that the function only returns `True` if exactly the specified table exists in the `stdout` string.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout
``` 

By splitting the `stdout` string into lines and checking if the table exists among those lines, we ensure that the function correctly identifies the existence of the specified table.