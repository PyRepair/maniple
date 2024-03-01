### Identified Bug:
The bug lies in the `table_exists` function of the `HiveCommandClient` class. The function does not perform a case-insensitive check when comparing the table name extracted from the `stdout` with the provided table name. This leads to test failures when the table names have different cases.

### Error Cause:
- The `table_exists` function compares the `table` variable directly with the table names extracted from `stdout`, without converting them to a consistent case (either upper or lower case).
- When the `table` variable and the table names extracted from `stdout` have different cases (e.g., 'MyTable' vs. 'mytable'), the comparison fails due to case sensitivity.

### Solution Strategy:
- To fix the bug, convert both the `table` variable and the table names extracted from `stdout` to a consistent case (e.g., lower case or upper case) before comparing them.
- Implement a case-insensitive comparison between the table names to ensure the function works correctly regardless of the case of the table names.

### Corrected Version of the Function:
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table.lower() in map(str.lower, stdout.splitlines())
        else:
            stdout = run_hive_cmd(
                """use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

            return bool(stdout)
```

### Changes Made:
- Converted both the `table` variable and table names extracted from `stdout` to lower case for comparison using `table.lower()` and `map(str.lower, stdout.splitlines())`.
- Changed the check to return `True` if `stdout` is not empty (regardless of the case) in the partition case to simplify the logic and improve readability.

By making these changes, the `table_exists` function should now work as expected and pass the failing tests related to case-insensitivity.