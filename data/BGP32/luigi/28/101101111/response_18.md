To fix the bug in the `table_exists` function and make it case insensitive, we need to modify how we compare the table name with the stdout. We should convert both to lowercase before comparison. Here is the corrected version of the function:

```python
class HiveCommandClient(HiveClient):

    def partition_spec(self, partition):
        # Please ignore the body of this function

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

            return stdout
```

By converting both `table` and `stdout` to lowercase before comparison, we ensure that the function is case insensitive and can correctly identify if a table exists in Hive regardless of the case.

This correction aligns with the proposed fix in the GitHub issue #896, which suggests making the `table_exists` function case insensitive by checking `stdout` against `table.lower()` to avoid case issues.