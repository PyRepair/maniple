### Bug Explanation:
The bug in the `table_exists` function lies in the comparison logic within the `if` conditions. In the first `if` block, the function checks if the table exists by verifying if the `table` string is present in `stdout`. However, when `stdout` is 'OK', the function incorrectly returns `True` because `'OK'` evaluates to `True` in a boolean context. This causes the test case where `table` is 'mytable' to fail.

In the second `if` block, the function checks if the `stdout` contains any data to determine the existence of the table. If `stdout` is not empty, the function incorrectly returns `True`, leading to the failure of the test case where `table` is 'MyTable'.

### Bug Fix:
To fix the bug, we should modify the return statements in both `if` blocks. Instead of directly returning the result of the comparison, we should explicitly check for the presence of the table in the `stdout` variable and return `True` only if it is found.

### Corrected Code:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return (stdout is not None and table in stdout)
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return (stdout is not None)
``` 

By making these changes, the `table_exists` function now correctly verifies the existence of the table and will return `True` only if the specified table is found in the `stdout` output.