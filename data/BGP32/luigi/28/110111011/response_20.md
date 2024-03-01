The bug in the `table_exists` function is due to a case sensitivity issue where the function checks if the table exists based on an exact match rather than a case-insensitive match. This leads to test failures when the table name cases don't match exactly.

To fix this bug and address GitHub issue #896, the function needs to compare the table name in a case-insensitive manner. One way to achieve this is by converting both the table name and the output from `run_hive_cmd` to lowercase for comparison.

Here is the corrected version of the `table_exists` function:

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

This corrected version converts both the `table` and `stdout` to lowercase for a case-insensitive comparison, ensuring that the function works as expected and passes the failing tests.

By making this change, the `table_exists` function will now handle case sensitivity properly and resolve the failing test cases.