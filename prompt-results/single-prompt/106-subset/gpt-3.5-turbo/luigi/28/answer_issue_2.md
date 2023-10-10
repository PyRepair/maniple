To fix the bug in the `table_exists` method, we can modify the line that performs the check against the stdout. Instead of checking if `table` is present in `stdout`, we can convert both `table` and `stdout` to lowercase and check if `table.lower()` is present in `stdout.lower()`. This will make the check case-insensitive.

Here's the fixed code snippet:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return stdout and table.lower() in stdout.lower()
```

With this fix, the `table_exists` method will correctly handle case-insensitive table names when checking against the stdout.

This patch can be easily applied to the original project by replacing the existing `table_exists` method with the fixed code snippet.