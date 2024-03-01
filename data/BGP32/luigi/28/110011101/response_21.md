### Bug Explanation
The bug in the `table_exists` function arises from the way the function checks the presence of the table in the `stdout` output. The function checks whether the table is exactly in the `stdout` output, which leads to the failure of the test cases where the table name is part of a larger string (`OK\ntable_name`). Additionally, the function does not handle case sensitivity correctly, causing inconsistencies in table existence checks.

### Bug Fix Strategy
To fix the bug, we need to modify the function in a way that correctly checks for the table's presence in the `stdout` output, regardless of its position within a string. We also need to ensure that the table existence check is case-insensitive.

### Corrected Version

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
            return True if stdout else False
```

In the corrected version:
- We convert both the `table` and `stdout` to lowercase before comparison to ensure case-insensitive matching.
- We check if the lowercased `table` is contained in the lowercased `stdout` to determine the table's existence.
- We simplify the `if else` block by directly returning the conditions instead of separate return statements.