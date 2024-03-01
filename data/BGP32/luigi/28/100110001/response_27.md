The bug in the `table_exists` function lies in how the return values from `run_hive_cmd` are being handled. The function is checking if the output contains the table name, but it should handle the cases where the table name is present in different formats as well.

The correct approach would be to split the `stdout` by newline characters and check if the table name is present in any of the lines.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

In this corrected version:
1. For the case when `partition` is `None`, we split the `stdout` by newline characters and directly check if the `table` is present in any line.
2. For the case when `partition` is not `None`, we return `bool(stdout)` which handles the case if `stdout` is not empty.

By making these changes, the function should now pass the failing test cases provided.