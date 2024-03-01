To fix the bug in the `table_exists` function, we need to modify the comparison between the `table` name and the `stdout` output to be case insensitive, as per the GitHub issue. By converting both the `table` name and the `stdout` output to lowercase before comparison, we can ensure that the check is not affected by case differences.

Here is the corrected version of the `table_exists` function:

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

By converting both the `table` and `stdout` to lowercase before comparison, we ensure that the function is case insensitive when checking for the existence of a table. This correction addresses the issue reported in GitHub and allows the function to pass the failing test cases while providing the expected behavior of case insensitivity in table existence checks.