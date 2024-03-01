The bug in the `table_exists` function is related to case sensitivity when comparing the table names. The function currently checks if the table name is exactly the same as the one returned in the `stdout` from the hive command. However, since hive is case insensitive, this comparison can fail when the cases do not match.

To fix the bug, we need to make the comparison case insensitive by converting both the table name and the output from `stdout` to lowercase before checking for equality.

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

With this correction, the function will now convert both the table name and the output from `stdout` to lowercase before comparing them, making the comparison case insensitive.

This fix addresses the issue raised in GitHub regarding making the `table_exists` function case insensitive, as suggested in the pull request for fixing issue #896.