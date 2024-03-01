To fix the bug in the `table_exists` function, we need to make the comparison case insensitive by converting both the table name and the stdout to lowercase before the comparison. This will ensure that the check is not affected by differences in case sensitivity.

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

By converting both the `table` and `stdout` to lowercase before the comparison, the function will now handle case sensitivity correctly. This correction will address the failing test cases and resolve the issue reported on GitHub related to making the `table_exists` function case insensitive.