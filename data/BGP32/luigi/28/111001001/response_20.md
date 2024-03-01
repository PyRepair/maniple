## Bug Analysis
The buggy function `table_exists` is checking for the existence of a table in a database with optional partition information. The bug seems to be related to how the function handles the output (`stdout`) of the `run_hive_cmd` function.

### Issue:
1. In Case 1 and Case 3, the function fails to correctly check if the table exists or not when the output is 'OK'. This is because the condition `stdout and table in stdout` only checks if `stdout` exists, not if the table is present in the output string.
2. In Case 2 and Case 4, the function fails to correctly handle case sensitivity for table names. The function does a simple string check without considering case sensitivity.

### Bug Cause:
1. The bug in Case 1 and Case 3 occurs because the function incorrectly checks for the existence of the table in the `stdout` string using the `and` condition.
2. The bug in Case 2 and Case 4 occurs due to a lack of case sensitivity handling when checking for the table name in the `stdout` string.

### Strategy for Fixing the Bug:
1. Modify the condition in the first part of the function to specifically check for the table name in the `stdout` string.
2. Implement a case-insensitive check for the table name in the `stdout` string.

### Corrected Version:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and any(t.lower() == table.lower() for t in stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

In the corrected version:
- The first part of the function uses a list comprehension to check if the table exists in a case-insensitive manner.
- The `any()` function is used to return `True` if any match is found in the `stdout` string.
- This approach addresses the issues identified in the buggy function and ensures proper table existence checks in a case-insensitive manner.