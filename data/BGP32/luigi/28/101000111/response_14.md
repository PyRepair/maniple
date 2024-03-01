To fix the bug in the `table_exists` function, we need to modify the comparison of the table name with the tables in stdout to be case insensitive. We will convert both the table name and the tables in stdout to lowercase before comparison.

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

This corrected version ensures that the comparison between the table name and tables in stdout is case insensitive by converting both strings to lowercase before comparison. This change aligns with the GitHub issue requesting a case-insensitive check for table existence in Hive.