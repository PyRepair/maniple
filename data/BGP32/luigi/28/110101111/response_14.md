### Bug Analysis:
1. The `table_exists` function in the `HiveCommandClient` class of `luigi/contrib/hive.py` is not handling case sensitivity properly. The function checks for an exact match between the input table name and the table names retrieved from Hive, leading to test failures due to case mismatch.
2. The issue reported on GitHub (#896) suggests making the `table_exists` function case insensitive by comparing the lowercase versions of table names.
3. The current implementation of the function does not consider case differences, causing the tests to fail when expected table names do not match the actual case of the tables in Hive.
4. To fix the bug, we need to modify the `table_exists` function to compare the lowercase versions of table names for a case-insensitive check.

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
- The updated `table_exists` function now converts both the input table name and the names retrieved from Hive to lowercase for a case-insensitive comparison.
- By comparing the lowercase versions of the table names, we ensure that the function behaves consistently regardless of the case of the table names in Hive.
- The function now returns `True` if the table is found in the Hive output, ignoring the case, and `False` otherwise.

### Result:
The corrected version of the `table_exists` function should pass all the failing test cases, making it case insensitive and resolving the issue reported on GitHub (#896).