### Analysis:
The buggy function `table_exists` is designed to check if a table exists in a given database. The issue reported on GitHub suggests that the function should be case insensitive, as the table names might differ in case.

The bug arises from the comparison between the table name and the output from the `run_hive_cmd` function, which may not match due to case sensitivity. The issue on GitHub provides a clear direction to fix this problem by making the comparison case insensitive.

### Bug Cause:
The bug occurs because the table name comparison in the `table_exists` function does not account for case sensitivity. When the table name case in the database differs from the input table name, the comparison fails. 

### Bug Fix Strategy:
To fix the bug, we need to modify the comparison between the table name and the output from the `run_hive_cmd` function to be case insensitive. We can achieve this by converting both strings to lowercase before comparing them.

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

In the corrected version, both the table name and the output from `run_hive_cmd` are converted to lowercase using the `lower()` method before the comparison. This change ensures that the comparison is case insensitive, resolving the reported issue.