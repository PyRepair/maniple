### Analysis:
1. The `table_exists` function in the `HiveCommandClient` class is not handling case sensitivity correctly, as discussed in the GitHub issue.
2. The bug occurs because the function is comparing the `table` name directly to the `stdout` without converting them to a consistent case.
3. The function should compare the lowercase version of the `table` with the lowercase version of the `stdout`.
4. To fix the bug, modify the comparison logic to use lowercase strings for comparison.

### Correction:
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
            stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

            if stdout:
                return True
            else:
                return False
```

### Explanation:
The corrected version of the `table_exists` function now converts both the `table` and `stdout` to lowercase before comparing, making the comparison case insensitive. This change addresses the issue reported on GitHub and aligns the function's behavior with the expected case sensitivity handling.