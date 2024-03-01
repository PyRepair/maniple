The bug in the `table_exists` function is that it does not handle case sensitivity when comparing table names. The `table_exists` function is checking if the given table exists in the list of tables retrieved from the `show tables like` command output. However, it directly compares the table names without considering case sensitivity.

To fix this issue, we need to make the comparison case insensitive by converting both the table name and the output from `run_hive_cmd` to lowercase before comparison.

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

By converting both the table name and the stdout to lowercase before comparison, we ensure a case-insensitive check for table existence.

This corrected version should address the issue raised in GitHub and pass all the failing test cases mentioned.