Based on the GitHub issue and the provided information, the bug in the `table_exists` function is related to the case sensitivity of table names. When checking if a table exists in Hive, the function does a direct comparison between the table name input and the table names obtained from Hive, which can cause failures due to case differences.

To fix this bug, we need to make the comparison case insensitive by converting both the table name and the names obtained from Hive to lowercase before comparison.

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
```

This corrected version converts both the `table` and the strings obtained from Hive to lowercase before the comparison, ensuring that the check is case insensitive.

By making this change, the function will now correctly handle case differences when checking for table existence in Hive, resolving the issue reported on GitHub.