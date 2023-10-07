Here is the fixed `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table.lower()))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table.lower(), self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

Modifications applied are:
1. Use `table.lower()` with the `run_hive_cmd` to ensure proper format.
2. Compare with `table.lower()` in `stdout.lower()` to ensure case-insensitivity when checking if the table exists.
These changes should fix the case sensitivity issue without affecting other tests and can be easily applied to the original project.