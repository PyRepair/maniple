To fix the bug, we need to modify the `table_exists` function to compare the table names in a case-insensitive manner. This can be achieved by converting both the table name and the output from the `run_hive_cmd` to lowercase before comparison.

Here's the corrected version of the `table_exists` function:

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By converting both the `table` and the `stdout` to lowercase before comparison, the function will now be case-insensitive when checking for table existence.

After making this change, the failing tests should now pass, and the issue reported on GitHub regarding case sensitivity in `table_exists` function should be resolved.