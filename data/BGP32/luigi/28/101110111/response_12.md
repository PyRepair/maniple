To fix the bug in the `table_exists` function, we need to make the comparison case-insensitive by converting both `table` and `stdout` to lowercase before checking for existence. Based on the failing test cases, we should modify the function to address this issue.

Here is the corrected version of the `table_exists` function:

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

By converting both `table` and `stdout` to lowercase using `lower()` before comparison, we ensure a case-insensitive check for table existence in the Hive output.

This corrected version of the function should pass all the failing test cases and satisfy the expected input/output values provided for each scenario. It also addresses the issue raised on GitHub (Fix #896: make table_exists case insensitive).