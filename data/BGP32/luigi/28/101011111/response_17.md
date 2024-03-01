To fix the bug in the `table_exists` function, we need to ensure that the comparison between the table name and the output from the Hive command is case insensitive.

Here's the corrected version of the `table_exists` function:

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

By converting both the table name and the output from the Hive command to lowercase during comparison, we ensure that the check is case insensitive.

With this correction, the function should now pass the failing test cases and satisfy the expected input/output values provided earlier. The fix also addresses the GitHub issue related to making the `table_exists` function case insensitive.