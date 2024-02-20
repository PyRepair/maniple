To fix the bug, the comparison of the table name with the table in the stdout must be made case-insensitive. This can be achieved by converting both `table` and `stdout` to lowercase before comparison.

Here's the corrected code for the `table_exists` function:

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

With this implementation, the comparison between the table name and the table in `stdout` will be case-insensitive. This should address the issue reported in the GitHub bug and allow the `table_exists` function to correctly identify whether a table exists in a specified database.