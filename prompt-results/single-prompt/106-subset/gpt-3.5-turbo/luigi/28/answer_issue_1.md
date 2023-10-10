Here is the fixed code snippet:

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

The bug was fixed by changing the condition `table in stdout` to `table.lower() in stdout.lower()`. This makes the comparison case-insensitive, allowing tables with different capitalizations to match correctly.

Additionally, the redundant check for `if stdout:` before returning `True` or `False` was removed, since `stdout` will already evaluate as truthy or falsy depending on its value.