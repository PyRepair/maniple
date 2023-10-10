To fix the bug and make the `table_exists` method case-insensitive, we can modify the conditional statement where we check if the table exists in the `stdout` output. We can use the `lower()` method to convert both the `table` and `stdout` to lowercase before performing the comparison.

Here's the modified code:

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

By converting both the `table` and `stdout` to lowercase, we can avoid any case issues and ensure that the method returns the correct result.

This fix allows the test case to pass by making the comparison case-insensitive.