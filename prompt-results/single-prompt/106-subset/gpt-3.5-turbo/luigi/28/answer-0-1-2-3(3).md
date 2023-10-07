To fix the bug, we need to modify the `table_exists` function to make it case insensitive when checking if the table exists in the output of the query.

Here is the fixed code:

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

By using `table.lower()` and `stdout.lower()`, we ensure that both the table name and the output are converted to lowercase before comparing.

With this fix, the `table_exists` function will now be case insensitive when checking if a table exists in the Hive database.