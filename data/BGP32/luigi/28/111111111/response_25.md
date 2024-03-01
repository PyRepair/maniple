To fix the bug in the `table_exists` function, we need to make the comparison case insensitive by converting both the table name and the stdout to lowercase before checking if the table exists. This will ensure that the function works correctly with table names that have different cases.

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

By converting both the table name and the stdout to lowercase before comparison, the function will now correctly handle case-insensitive table name checks. This change aligns with the suggested fix mentioned in the GitHub issue #896.

After applying this correction, the function should pass the failing tests provided and behave as expected in the given scenarios.