Based on the GitHub issue and the failing test cases, the bug in the `table_exists` function is that it does not handle case insensitivity correctly when comparing the table names. The function needs to convert both the table name and the output from `run_hive_cmd` to lowercase before comparison to ensure case-insensitive matching.

Here is the corrected version of the function:

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

In the corrected version, both the `table` and `stdout` variable are converted to lowercase using the `lower()` method before performing the comparison. This change will ensure that the comparison is case insensitive and will fix the bug reported in the GitHub issue.

With this correction, the `table_exists` function should pass all the failing test cases provided, including the case sensitivity test case outlined in GitHub issue #896.