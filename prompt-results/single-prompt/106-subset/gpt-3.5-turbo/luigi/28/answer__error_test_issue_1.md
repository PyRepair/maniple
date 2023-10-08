To fix the bug in the `table_exists` method in the `HiveCommandClient` class, we can modify the existing code by converting both `stdout` and `table` to lower case before comparing them. This will make the comparison case-insensitive.

Here's the modified code snippet:

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

With this modification, the `table_exists` method will now compare the lower case version of `table` with the lower case version of `stdout`, allowing case-insensitive matching. This should fix the bug described in the issue.