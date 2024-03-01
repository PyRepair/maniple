The bug in the `table_exists` function is due to case sensitivity when comparing the table name with the result from `run_hive_cmd`. As mentioned in the GitHub issue, sometimes tables are defined with capitalized names, but Hive returns them in lowercase. Therefore, the check in the function fails due to case mismatch.

To fix this bug, we need to modify the comparison to be case insensitive. We can achieve this by converting both the table name and the result from `run_hive_cmd` to lowercase before comparing them.

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

In this corrected version:
- We convert both the `table` and `stdout` to lowercase before comparing them using `table.lower() in stdout.lower()`.
- We use `bool(stdout)` directly as the return value when checking the partition, as it will return `True` if `stdout` is not empty.

By making these changes, we address the case sensitivity issue identified in the GitHub issue. The function now properly checks for table existence regardless of the case of the table name.