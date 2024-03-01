### Problem Analysis:
1. The function `table_exists()` is currently case sensitive when checking if a table exists in Hive.
2. The bug arises when tables have different casing than what is checked, leading to false negatives.
3. The GitHub issue suggests making the comparison case insensitive to handle this issue effectively.

### Bug Cause:
- The bug stems from the direct comparison between the table name and the stdout without considering the case sensitivity of the names.

### Bug Fix Strategy:
To fix the bug, we need to lowercase both the table name and the stdout before comparing them to ensure a case-insensitive check.

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

By making this adjustment to the function, the comparison will now be case insensitive, resolving the issue highlighted in the GitHub reports.