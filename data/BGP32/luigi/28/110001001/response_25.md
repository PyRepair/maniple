### Explanation of the bug
The bug in the `table_exists` function is related to how the function checks if a table exists in a given database. The bug occurs when the function is provided with a table name that differs in case from the actual table name in the database. The function uses a case-sensitive check to determine if the table exists, which leads to incorrect results when the case of the input table name does not match the case of the actual table name in the database.

### Bug's Cause
The bug is caused by the comparison between the `table` parameter and the `stdout` output. When the table name in the database is in a different case than the one provided as input, the comparison fails due to case sensitivity, resulting in a false negative (table not found when it actually exists).

### Strategy for fixing the bug
To fix the bug, we need to modify the comparison between the `table` parameter and the `stdout` output to perform a case-insensitive check. This way, we can accurately determine if the table exists regardless of the case of the table name.

### Corrected Version of the function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
```

In the corrected version of the function, the comparison is done by converting both the `table` parameter and the elements in `stdout` to lowercase before checking if the `table` exists in the `stdout`. This ensures that the table name case sensitivity does not affect the result of the comparison. Additionally, the `stdout` is directly converted to a boolean value for easier handling.