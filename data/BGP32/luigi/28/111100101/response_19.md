### Analysis:
- The function `table_exists` in the `HiveCommandClient` class is intended to check if a specific table exists in a given database. It uses the `run_hive_cmd` function to execute Hive commands.
- The bug seems to be related to the comparison of the table name in the standard output (`stdout`) returned by the Hive command.
- In the case where a partition is provided, the function also calls `self.partition_spec(partition)` to generate the partition spec to include in the Hive command.
- The function does not handle case sensitivity when comparing table names.

### Bug Explanation:
- The bug occurs because the `table_exists` function does not take into account case sensitivity when comparing the table names obtained from the Hive command output (`stdout`). This results in incorrect evaluations of table existence.

### Bug Fix:
To fix the bug, we need to modify the comparison of table names in the `stdout` by making it case-insensitive.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        table_lower = table.lower()
        return stdout and table_lower in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                            ({2})""".format(database, table, self.partition_spec(partition)))
        return bool(stdout)
```

By converting both the input table name and the names in `stdout` to lowercase for comparison, we ensure that the function is case-insensitive. This corrected version should pass the failing test cases provided.