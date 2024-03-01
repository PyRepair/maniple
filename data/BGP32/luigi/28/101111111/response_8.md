The bug in the `table_exists` function arises from the case sensitivity when comparing the table name with the output from the hive command. To fix this issue, we need to modify the comparison to be case insensitive.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table.lower()))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                             (%s)""" % (database, table.lower(), self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By changing the comparison to `table.lower() in stdout.lower()`, we ensure that the comparison is case insensitive, which addresses the failing tests and the GitHub issue raised.