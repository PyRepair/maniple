## Fixing the bug in the `table_exists` function

### Issue:
The `table_exists` function in the `HiveCommandClient` class has a bug where it does not handle table names with different cases correctly. This results in failing tests when checking for table existence with different case variants.

### Cause of the bug:
The bug stems from the fact that the function compares the table name directly with the output of the `run_hive_cmd` function without considering the case sensitivity of the table names.

### Strategy for fixing the bug:
To fix the bug, we need to modify the comparison of the table name with the output of `run_hive_cmd` to be case insensitive. We can achieve this by converting both the table name and the output to lowercase before comparison.

### Updated `table_exists` function:
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
            stdout = run_hive_cmd(
                """use {0}; show partitions {1} partition ({2})""".format(database, table, self.partition_spec(partition)))

            return bool(stdout)
```

By converting both the table name and the output to lowercase before comparison, the `table_exists` function will now be case-insensitive when checking for table existence.

This fix addresses the reported GitHub issue #896.