To fix the bug in the `table_exists` function, we need to modify the comparison of the table name in the output `stdout` to be case-insensitive. This can be achieved by converting both `table` and `stdout` to lowercase before comparison.

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

By converting both `table` and `stdout` to lowercase before comparison, we ensure that the check is case-insensitive and the function should now pass the failing test cases provided.

This fix addresses the issue reported in GitHub related to making the `table_exists` function case-insensitive to match the behavior of Hive.