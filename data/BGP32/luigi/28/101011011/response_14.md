### Explanation:
The bug in the `table_exists` function is related to case sensitivity. The function compares the provided table name with the output from the Hive command without considering case differences, leading to test failures when the cases do not match.

The failing tests demonstrate this issue by using different cases for the table name and expecting a case-insensitive comparison result. The function should convert both the table name and the output from the Hive command to the same case (e.g., lowercase) for proper comparison.

### Bug Fix Strategy:
To fix the bug, modify the `table_exists` function to convert both the table name and the output from the Hive command to lowercase (or any consistent case) before comparison. This adjustment will ensure a case-insensitive check when verifying table existence.

### Corrected Version:
```python
# Updated table_exists function with case-insensitive check

def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                              (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

In the corrected version, both the `table` and the `stdout` are converted to lowercase for the comparison, ensuring a consistent case check and resolving the case sensitivity issue identified in the failing tests.