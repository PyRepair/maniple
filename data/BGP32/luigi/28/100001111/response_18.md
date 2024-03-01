The bug in the `table_exists` function lies in the comparison of the table name with the output from the Hive command. The comparison is case-sensitive, causing failures when the case of the table name in the code does not match the case in the Hive output.

To fix the bug, the comparison should be case-insensitive by converting both the table name and the Hive output to lowercase before checking for existence.

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

With this correction, the function will now compare the lowercase versions of the table name and the Hive output, making the comparison case-insensitive and resolving the issue reported on GitHub.