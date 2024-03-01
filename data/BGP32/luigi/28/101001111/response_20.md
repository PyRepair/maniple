The buggy function `table_exists` has an issue related to case sensitivity, where it doesn't match the table name case-insensitively when checking if a table exists in the Hive database. This bug is causing test failures due to the mismatch in expected and actual case of table names.

### Bug Explanation:
The bug in the function `table_exists` is that it directly compares the table name without considering the case sensitivity of the table names in Hive. This leads to failures in tests where the case of the table name doesn't match exactly.

### Bug Fix Strategy:
To fix this bug, we need to modify the comparison logic to be case-insensitive. We can convert both the table name and the output from Hive to lowercase and then check if the table name exists in the output effectively ignoring the case.

### Corrected Version of the Function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd(f"use {database}; show partitions {table} partition ({self.partition_spec(partition)})")

        return bool(stdout)
```

In the corrected version:
1. We convert both the `table` and `stdout` to lowercase before comparison in case-insensitive manner.
2. For the else case where partitions are involved, the return is simplified by directly returning a boolean value based on the existence of `stdout`.

This corrected version is aligned with the expected behavior described in the failing tests and also addresses the case sensitivity issue reported in the GitHub issue.