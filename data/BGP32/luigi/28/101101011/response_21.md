To fix the bug in the `table_exists` function, we need to make the table comparison case-insensitive by converting both `table` and `stdout` to lowercase before checking for equality. This change will address the issue reported on GitHub and ensure that the function works correctly with tables regardless of their case.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
        return bool(stdout)
```

In this corrected version:
- The `table` and `stdout` strings are converted to lowercase using the `lower()` method.
- The comparison `table.lower() in stdout.lower()` is used to check if the table exists in the stdout output regardless of case sensitivity.

By implementing these changes, the `table_exists` function should now pass the failing test cases and address the reported issue on GitHub related to case insensitivity.