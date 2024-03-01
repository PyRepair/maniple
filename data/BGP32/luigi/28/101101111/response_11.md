To fix the bug in the `table_exists` function, we need to make the comparison case-insensitive by converting both the table name and the output from Hive to lowercase before checking for existence. This will address the issue reported in GitHub.

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

By converting both the `table` and `stdout` to lowercase before comparing, we ensure that the function is case-insensitive and can handle variations in capitalization as seen in the failing test cases.

This fix aligns with the suggested strategy in the GitHub issue to make the `table_exists` function case insensitive.