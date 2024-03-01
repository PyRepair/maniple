### Bug Explanation
The bug in the `table_exists` function lies in the conditional check for the existence of a table in the Hive database. The function incorrectly returns `False` when it should be returning `True` in certain cases, leading to failing test cases.

In the first case, when the `table` exists in the database and is found in the `stdout`, the function should return `True`, but it incorrectly returns `False`.

In the second case, when the `table` exists in the database and is found in the `stdout`, the function should return `True`, but it incorrectly returns `False`.

### Strategy to Fix the Bug
To fix the bug, we need to ensure that the function correctly evaluates the conditions and returns the expected boolean values based on whether the table exists in the database or not. We need to adjust the logic in the function to return `True` when the table is found in the `stdout` and `False` otherwise.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

After applying these changes, the corrected function should now return `True` when the table is found in the `stdout` and `False` otherwise, as expected.