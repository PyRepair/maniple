### Analysis:
1. The `table_exists` function within the `HiveCommandClient` class checks if a table exists in a specified database using a Hive command.
2. The bug occurs due to case sensitivity in comparing the table name from the command output.
3. The bug arises from not converting the table name to lowercase before comparing with the output. This results in assertion failures in the test cases, as the comparison is case sensitive.
4. The strategy to fix the bug is to convert both the table name and the output to lowercase before comparison.
5. The corrected version of the function should ensure that the comparison is case insensitive.

### Code Fix:
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
1. The corrected `table_exists` function calls `lower()` on both the `table` and the `stdout` before comparison to make the check case insensitive.
2. In the case where `partition is None`, it checks if the lowercase of the table name is present in the lowercase of the command output.
3. The `bool(stdout)` ensures that the function returns True if the stdout is not empty, which simplifies the function logic and makes it more robust.
4. This fix addresses the case sensitivity issue reported in the GitHub issues #896 and resolves the failing test cases by making the comparison case insensitive.