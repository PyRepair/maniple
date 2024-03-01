### Bug Explanation
The bug in the `table_exists` function lies in the way the return value is checked. The function is supposed to check if the table exists in the output of the Hive command, but it mistakenly checks if the table name is directly in the output without considering the formatting.

### Bug Location
The bug occurs in the comparison statements `table in stdout` and the existence check for the table name in the output.

### Bug Fix Strategy
To fix the bug, we need to correctly parse the output of the Hive command to ensure that the table name exists in the correct format within the output.

### Corrected Version
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

            # Checking if the table exists in the list of tables in the stdout
            return stdout and table in stdout.split('\n')
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

            # Checking if the table name is present in the partitions output
            return stdout and table in stdout
```

### Modifications
1. Split the `stdout` by newline character `\n` to get a list of tables for comparison in the `if partition is None` case.
2. Directly check if the `table` name is in the `stdout` for the `else` case where partitions are shown.

By making these changes, the function should correctly identify if the table exists in the output of the Hive command, fixing the bug.