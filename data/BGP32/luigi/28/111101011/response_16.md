The bug in the `table_exists` function is due to case sensitivity when comparing the table name from the `stdout` with the provided table name. The current implementation does a direct string comparison without considering case differences, leading to test failures when the case of the table name is different in the `stdout`.

To fix the bug, we need to modify the comparison logic to be case insensitive. One way to achieve this is by converting both the table name and the `stdout` value to lowercase before comparison.

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

By converting both `table` and `stdout` to lowercase before comparison, we ensure that the function is case insensitive, addressing the issue reported on GitHub (#896).

This corrected version of the function should now pass the failing test cases provided.