The buggy function `table_exists` currently has a case sensitivity issue as reported in the GitHub issue. It fails to account for the case sensitivity of the table names when checking for table existence. To fix this issue, we need to modify the function to make it case insensitive by comparing the table name in a case-insensitive manner.

Here's the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.splitlines())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By modifying the return statement to check `table.lower() in map(str.lower, stdout.splitlines())`, we ensure that the table names are compared in a case-insensitive manner. This change addresses the reported issue and makes the function more robust in handling different table name cases.