### Analysis:
1. The `table_exists` function in the `HiveCommandClient` class is supposed to check if a table exists in the specified database. However, the comparison between the table name and the output from `run_hive_cmd` is case-sensitive, leading to test failures.
2. The bug arises when comparing the table name with the output without normalizing case, causing the function to fail when there are differences in case sensitivity.
3. The failing test cases provide input values for the function and the expected behavior. The function fails to handle case-insensitive table existence checks correctly due to direct string comparison without case normalization.
4. To fix the bug, we need to compare the normalized case versions of the table name and the output from `run_hive_cmd` to ensure case insensitivity in the comparison.

### Bug Fix:
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

### Explanation:
1. Modified the comparison in the `table_exists` function to compare the lowercased versions of the table name and the output from `run_hive_cmd`.
2. By normalizing the case for both strings, we ensure a case-insensitive comparison for table existence checks.
3. The use of `table.lower()` and `stdout.lower()` in the comparison addresses the case sensitivity issue reported in the failing tests.
4. With this fix, the `table_exists` function should now correctly handle case-insensitive table existence checks.