The bug in the `table_exists` function lies in the comparison between the table name and the tables returned in the `stdout`. The issue arises because the table names in `stdout` are always returned in lowercase due to Hive being case insensitive, causing the comparison to fail when the provided table name is capitalized.

To fix this bug, we need to convert both the table name and the tables from `stdout` to lowercase before comparison.

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

By converting both the table name and the tables from `stdout` to lowercase before comparison, the function will now correctly identify the table's existence regardless of case sensitivity, as requested in the GitHub issue.