The bug in the `table_exists` function arises from a mismatch in the case sensitivity of table names when checking if a table exists in the Hive database. The function currently compares the table name directly with the tables retrieved from the Hive, leading to failures when there are case differences.

To fix this issue, we need to make the table comparison case insensitive by converting both the table name and the retrieved tables to lowercase before comparison.

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

In this corrected version:
- The `table.lower()` converts the input table name to lowercase for case-insensitivity.
- The `map(str.lower, stdout.split())` converts all table names retrieved from Hive to lowercase for comparison.

By making these changes, the function will now properly check for the existence of a table in a case-insensitive manner, resolving the issue reported on GitHub.