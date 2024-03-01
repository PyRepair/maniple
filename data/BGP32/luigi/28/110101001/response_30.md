### Bugs identified:
1. The function is not handling case sensitivity properly when checking if a table exists.
2. The function is not correctly handling the partition parameter when checking if a table exists.

### Bug explanation:
In the failing test cases, the function is failing to return the correct result because it does not handle case sensitivity for table names and does not properly construct the command when a partition is specified. This causes the function to incorrectly determine whether a table exists or not.

### Strategy for fixing the bug:
1. To handle case sensitivity, convert both the `table` parameter and the `stdout` output to lowercase before comparing them.
2. When a partition is specified, the function should construct the `run_hive_cmd` command correctly to include the partition information.

### Corrected version of the function:
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
            partition_str = self.partition_spec(partition)
            stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, partition_str))

            return bool(stdout)
```

By making the adjustments mentioned above in the corrected version of the function, it should now pass the failing test cases and correctly determine whether a table exists in Hive.