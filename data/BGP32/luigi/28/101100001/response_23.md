The bug in the `table_exists` function is caused by the condition checking for the presence of the table name in the output of the `run_hive_cmd` function. The current condition checks for whether the table name is a substring of the output, which leads to incorrect results when the table name is present in a larger string.

To fix this bug, we can split the output of `run_hive_cmd` by newline characters ('\n') and check if the table name is present in any of the lines.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

With this correction, the `table_exists` function should now pass the failing test cases.