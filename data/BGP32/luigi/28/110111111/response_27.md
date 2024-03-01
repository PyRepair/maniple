The bug in the `table_exists` function is due to case sensitivity when checking if the table exists in the `stdout`. The function directly compares the table name with the output from the Hive command, leading to false negatives when the case of the table name does not match the output case.

To fix this bug, we need to make the comparison case insensitive. We can achieve this by converting both the table name and the `stdout` to lowercase before comparison.

### Corrected Version of `table_exists` function:
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))

            return bool(stdout)
```

By converting both the `table` and `stdout` to lowercase before comparison, the corrected function will now provide the expected behavior for the `table_exists` function, passing the failing tests and addressing the case sensitivity issue reported in the GitHub issue #896.