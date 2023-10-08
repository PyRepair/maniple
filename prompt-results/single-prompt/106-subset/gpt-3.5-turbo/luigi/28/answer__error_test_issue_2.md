To fix the bug and make the `table_exists` function case insensitive, you can modify the comparison `table in stdout` to `table.lower() in stdout.lower()`. This will ensure that the comparison is not affected by the case of the table name.

Here's the modified code:

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

With this change, the `table_exists` function will perform a case insensitive comparison when checking if the table name is in the `stdout` response.

Hope this helps!