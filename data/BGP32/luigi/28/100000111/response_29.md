Based on the GitHub issues provided, the problem with the `table_exists` function is that it is case-sensitive in comparing table names which may cause test failures.

### Bug Explanation:
The bug lies in the comparison between the table name and the table names in the stdout, which can be case-sensitive. Since Hive is case-insensitive, the function should compare the lowercase version of the table name with the lowercase version of the names in stdout to prevent any issues.

### Fix Strategy:
To fix the bug, we need to modify the comparison logic to use lowercase versions of the table names for comparison instead of the original case. This change will ensure a case-insensitive comparison.

### Corrected Code:
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

By making this modification to the function, it should now correctly handle case-insensitive table name comparisons as expected in the GitHub issues.