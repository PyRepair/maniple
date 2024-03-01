### Analysis
The `table_exists` function in the `HiveCommandClient` class is supposed to check if a table exists in a given database. However, there are issues in the implementation that are causing failures in the test cases.

### Error Locations
1. Incorrect comparison logic in the `if partition is None` block.
2. Incorrect formatting of the command string in the `else` block.
3. Lack of validation for the response from the `run_hive_cmd` function.

### Bug Explanation
1. In the first case, the function should return `False` only if the table is not found in the `stdout`, but the current implementation returns `True` if `stdout` is not empty.
2. In the second case, the function fails to properly format the query in the `else` block, leading to incorrect command execution.
3. Lack of validation in handling the response from `run_hive_cmd` can cause unexpected behavior if the command fails.

### Strategy for Fixing the Bug
1. Update the comparison logic in the `if partition is None` block to return `False` only when the table is not found in the `stdout`.
2. Fix the command string formatting in the `else` block to execute the correct query.
3. Check the response from `run_hive_cmd` before making any decisions based on it.

### Corrected Version
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table in stdout
        else:
            partition_str = self.partition_spec(partition)
            stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2});""".format(database, table, partition_str))
            return bool(stdout)
```

By making the above changes, the `table_exists` function should now properly handle the cases outlined in the failing test and return the expected values.