### Analysis:
1. The `table_exists` function is intended to check if a table exists in a database.
2. The issue reported on GitHub indicates that the function should be case insensitive in comparing table names due to differences in capitalization.
3. The failing test cases provide scenarios where the table names are compared with different capitalizations which the function does not handle properly.

### Bug Cause:
The bug is caused by the function not considering case insensitivity when comparing the table name with the output from Hive queries. The function compares the table name directly, leading to failures when the case does not match.

### Bug Fix:
To fix the bug, we need to modify the comparison between the table name and the output from Hive queries to be case insensitive.

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

By converting both the table name and the output to lowercase during comparison, the corrected function is now case insensitive, addressing the bug reported.