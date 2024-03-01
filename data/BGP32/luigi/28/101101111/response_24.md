To fix the bug in the `table_exists` function, we need to make the comparison case-insensitive by converting both `table` and `stdout` to lower case before checking for existence.

Here is the corrected version of the `table_exists` function:

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

By converting both `table` and `stdout` to lowercase using the `lower()` method before comparing them, we ensure that the comparison is case-insensitive and the function will now pass the failing test cases.

This correction addresses the issue raised in GitHub where table names are sometimes defined in capitalized format, leading to case sensitivity problems during comparison.