To fix the bug in the `table_exists` function and make it case-insensitive, we need to modify the comparison between `table` and `stdout` to ignore the case. This will ensure that the function correctly identifies the table's existence regardless of the case.

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

In this corrected version, both the `table` and `stdout` strings are converted to lowercase using the `lower()` method before comparing them. This change ensures that the comparison is case-insensitive, addressing the issue reported in the GitHub bug.

With this modification, the `table_exists` function should now pass the failing test cases and correctly handle table existence checks in a case-insensitive manner.