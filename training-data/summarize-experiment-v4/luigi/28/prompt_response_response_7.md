To fix the bug in the `table_exists` function, we need to update the comparison between the `table` parameter and the output `stdout` to be case insensitive. This can be achieved by converting both the `table` parameter and the `stdout` output to lowercase before comparing them.

Here is the corrected code for the `table_exists` function:

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

With this update, the `table_exists` function will now perform a case-insensitive comparison between the `table` parameter and the `stdout` output, allowing it to accurately determine whether the specified table exists in the specified database, regardless of the case of the table name.