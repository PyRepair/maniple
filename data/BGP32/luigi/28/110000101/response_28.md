### Analysis
The buggy function `table_exists()` is responsible for checking if a table exists in a given database, with the option to specify a partition. The function calls `run_hive_cmd()` to execute Hive commands and determine the existence of the table/partition. The bug seems to be related to the conditional statements for handling partitions.

### Potential Error Locations
1. Incorrect formatting or missing parameters in the Hive command string.
2. Incorrect logic in the conditional statements that check the output of `run_hive_cmd()`.

### Cause of the Bug
The bug occurs due to incorrect formatting of the Hive command string in the `else` block when handling partitions. The string formatting is not properly done, which causes the Hive command to fail and return incorrect results.

### Strategy for Fixing the Bug
To fix the bug, we need to ensure that the Hive command strings are correctly formatted and include all necessary parameters in both branches of the conditional statement. Additionally, we need to verify that the comparison with the `stdout` variable is accurate to determine if a table/partition exists.

### Corrected Version of the Function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, self.partition_spec(partition)))
        return stdout and '0 rows' not in stdout
```

In the corrected version:
- The Hive command strings in both branches are correctly formatted using `str.format()`.
- The `stdout` comparison ensures that the output contains the table/partition information, rather than just checking if it exists.
- The `return` statement in the `else` block checks for the presence of '0 rows' in the output to determine if the partition exists.

By making these changes, the function should now correctly check for the existence of tables and partitions in the specified database.