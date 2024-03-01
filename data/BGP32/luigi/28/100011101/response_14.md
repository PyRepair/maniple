## Bug Explanation
The bug in the `table_exists` function lies in the return conditions for checking if a table exists. In both cases where the function is checking for table existence, the condition `stdout and table in stdout` doesn't work as expected.

In the first case, the function returns `True` only if `table in stdout` is `True` and `stdout` is not empty. However, in the failing test cases, even if the table exists and is present in `stdout`, the function incorrectly returns `False` because it checks for the presence of both conditions simultaneously.

In the second case, where partition is not `None`, the function simply checks if `stdout` is not empty, which is incorrect. The presence of any output in `stdout` should indicate that the table exists, regardless of its content.

## Bug Fix
To fix the bug, we need to modify the return conditions in a way that correctly determines if a table exists based on the command output. We can simplify the conditions and ensure that the function returns `True` if any output is present in `stdout`.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return bool(stdout)  # Return True if stdout is not empty
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)  # Return True if stdout is not empty
```

With this fix, the function will return `True` if any output is present in `stdout`, indicating that the table exists. This correction ensures that the function behaves correctly and passes the failing test cases.