### Bug Analysis
- The bug occurs when the function `table_exists` is called with the table name in lowercase and then in uppercase. The function fails to consider case insensitivity in comparing the table names.
- The expected behavior is that the function should return `True` when the table name is found in the output of the Hive command.
- The bug is caused by comparing table names without considering the case sensitivity.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison of table names in the output of the Hive command to be case insensitive. This can be achieved by converting both the table names and the output to lowercase before comparison.

### Corrected Version
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

By converting both the table name and the output of the Hive command to lowercase before comparison, the corrected function now handles case insensitivity correctly. This modification ensures that the function behaves as expected in all the provided test cases.