The buggy function `table_exists` has a bug that causes it to be case-sensitive when checking if a table exists in Hive. The issue reported on GitHub (#896) suggests that the function should be case-insensitive when checking if a table exists.

### Error Location:
The bug is present in the comparison operation `table in stdout` in the first block of the `table_exists` function. This comparison is case-sensitive and does not account for variations in the case of table names.

### Cause of the Bug:
The bug occurs because the comparison `table in stdout` does not take into account the case of the table names in Hive, leading to false negatives when checking for table existence.

### Bug Fix Strategy:
To fix the bug, we need to convert both the table name and the output from Hive to lowercase before comparison. This way, we ensure a case-insensitive comparison, which aligns with the expected behavior according to the GitHub issue.

### Corrected Version of the Function:
Here is the corrected version of the `table_exists` function:

```python
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

By converting both the table name and the output to lowercase before comparison, the function now performs a case-insensitive check for table existence in Hive. This corrected version should pass all test cases and satisfy the expected input/output values, resolving the issue reported on GitHub.