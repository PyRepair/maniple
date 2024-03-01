To fix the bug in the `table_exists` function, we need to address the case sensitivity when comparing the table name in the stdout. Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

In the corrected version, before checking `table in stdout`, both `table` and `stdout` are converted to lowercase using the `lower()` method. This modification makes the comparison case-insensitive and ensures that the test cases for table existence pass regardless of the casing.

This fix addresses the issue raised in the GitHub ticket #896 and improves the robustness of the function for case-insensitive table name comparisons.