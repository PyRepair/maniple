The bug in the `table_exists` function lies in the comparison between the table name and the stdout from the `run_hive_cmd` function. The bug occurs due to case sensitivity, where the function fails to properly identify the table name in stdout if the case is different.

To fix this issue, we need to make the comparison case-insensitive by converting both the table name and the stdout to lowercase before checking for existence.

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

By converting both the table name and the stdout to lowercase before comparison, the function will correctly identify the table even if the case is different.

This correction aligns with the suggested fix in the GitHub issue #896 to make `table_exists` case insensitive.