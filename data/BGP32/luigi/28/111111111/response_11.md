To fix the bug in the `table_exists` function, we need to make the comparison case-insensitive. The function should compare table names in a case-insensitive manner to handle cases where the table names are in different cases.

Here is the corrected version of the function:

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

By using `table.lower()` and `stdout.lower()` when checking for the table name in the output, we ensure that the comparison is case-insensitive.

This fix will address the failing tests that were failing due to case sensitivity issues with table names in the `table_exists` function.