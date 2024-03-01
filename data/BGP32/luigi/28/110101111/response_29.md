### Analysis:
1. The buggy function `table_exists` in the `HiveCommandClient` class has a bug when checking for table existence, particularly when comparing the table name with the output from `run_hive_cmd`. This bug leads to inconsistent results due to case sensitivity issues.
2. The issue reported in GitHub (#896) highlights the necessity of making the `table_exists` function case insensitive.
3. The bug arises from direct comparison without considering case sensitivity, causing test failures when the table names differ in case.
4. To fix the bug, we need to modify the comparison logic to make it case insensitive, ensuring consistent behavior across different table name cases.

### Solution:
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

By modifying the comparison to `table.lower() in stdout.lower()`, the function will now be case insensitive when checking for table existence. This fix aligns with the reported GitHub issue #896 to ensure consistent behavior across different table name cases.