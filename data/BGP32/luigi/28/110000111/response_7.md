The buggy function `table_exists` in the `HiveCommandClient` class has a bug where it doesn't handle case sensitivity correctly when checking if a table exists in the database. The issue was reported on GitHub with the title "hive table_exists should be case insensitive?" and "Fix #896: make table_exists case insensitive".

The bug causes the function to fail when the table name has a different case than the one returned by Hive, leading to incorrect results.

### Error Analysis:
The buggy function has the following issues:
1. It directly checks if the table name is in the stdout without considering case sensitivity.
2. The function doesn't convert both the table name and stdout to lowercase for a case-insensitive comparison.

### Bug Cause:
The bug occurs because the function tries to match the exact case of the table name with the output received from Hive, which may not match due to case differences.

### Bug Fix Strategy:
To fix the bug, we need to convert both the table name and the output from Hive to lowercase before doing the comparison.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By converting both the table name and the output to lowercase in the comparison, the function will be able to handle case sensitivity correctly and address the issue reported on GitHub.