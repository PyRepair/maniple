The bug in the `table_exists` function is due to the comparison of the table names being case-sensitive. To resolve this issue, we need to make the comparison case-insensitive by converting both the table name and the stdout to lowercase before comparing them.

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

This corrected version ensures that the comparison between the table name and the output from `run_hive_cmd` is case-insensitive, fixing the failing tests related to the issue described in GitHub.