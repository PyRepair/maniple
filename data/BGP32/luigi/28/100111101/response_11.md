### Bug Fix Strategy:
The bug in the `table_exists` function seems to be related to how the function checks if a table exists based on the output of the `run_hive_cmd` function. The function returns `True` only if the table name is found in the output, leading to incorrect results in some test cases.

To fix the bug, we should modify the function to properly parse the output of `run_hive_cmd` and check if the table name is present in the expected format (taking case insensitivity into account in the process).

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout is not None and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By using the above corrected function, the `table_exists` method should now properly check if a table exists in the specified database and handle cases of case insensitivity. This should enable the function to pass the failing test cases.