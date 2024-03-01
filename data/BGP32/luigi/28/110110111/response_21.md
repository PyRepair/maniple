To fix the bug in the `table_exists` function, we need to make the comparison case-insensitive by converting both the `table` and the output from `run_hive_cmd` to lowercase before checking for existence.

Here is the corrected version of the `table_exists` function:

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

By converting both the `table` name and the `stdout` from `run_hive_cmd` to lowercase for comparison, we ensure that the comparison is case-insensitive and matches the expected behavior described in the GitHub issue #896.

This corrected version should pass all the failing test cases and fulfill the expected input/output values.