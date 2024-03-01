To fix the bug in the `table_exists` function, we need to make the comparison case insensitive by converting both the table name and the output from `run_hive_cmd` to lowercase before the comparison. This will ensure that the check for table existence is not affected by case discrepancies.

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

By converting both the table name and the output to lowercase before comparing them, we ensure that the function is case insensitive when checking for table existence.

This correction will address the failing test cases and align with the expected behavior described in the GitHub issue.