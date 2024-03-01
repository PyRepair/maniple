### Analysis:
1. The `table_exists` function checks if a given table exists in a specified database. The bug occurs when the table name capitalization doesn't match between the input and the returned `stdout`.
2. The issue reported on GitHub suggests that the function should be case insensitive while comparing the table name.
3. The bug arises because the function compares the exact table name with the `stdout`, which might not match in cases of different capitalizations.
4. To fix the bug, we need to convert both the table name and the `stdout` to lowercase for comparison.

### Bug Fix Strategy:
- Modify the function to convert both the table name and the `stdout` to lowercase before comparison.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

This corrected version ensures that the comparison between the table name and the `stdout` is case insensitive, resolving the reported bug.