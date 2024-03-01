### Bug Analysis:
1. The `table_exists` function within the `HiveCommandClient` class is not handling case insensitivity properly when checking if a table exists in the database.
2. The failing test case `test_table_exists` is failing due to incorrect comparison of table names.
3. The error message indicates that the assertion `self.assertTrue(returned)` is failing because the returned value is `False` instead of `True`.
4. The GitHub issue (#896) and the corresponding description suggest that the `table_exists` function should consider case insensitivity while checking for table existence.

### Bug Fix Strategy:
1. Modify the `table_exists` function to convert both the `table` and the `stdout` to lowercase for comparison to handle case insensitivity.
2. Apply this modification to both the standard and partitioned table existence checks.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

With this modification, the `table_exists` function should now handle case insensitivity properly and pass the failing test cases.