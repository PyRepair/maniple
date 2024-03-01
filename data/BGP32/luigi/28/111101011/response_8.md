The bug in the `table_exists` function is related to case sensitivity when checking if a table exists in Hive. The function currently checks if the table name is exactly the same as the output from the `run_hive_cmd` function, leading to failures with case differences.

To fix this bug, we need to make the comparison case-insensitive by converting both the table name and the stdout to lowercase before checking for existence.

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

By converting both the table name and the stdout to lowercase before comparison, the function will now correctly identify the table's existence without being affected by case differences.

This fix aligns with the GitHub issue #896 proposing to make the `table_exists` function case-insensitive for proper table existence checks.