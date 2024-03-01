### Analysis:
1. The buggy function checks if a table exists in a Hive database using a case-sensitive comparison, leading to test failures when table names are capitalized differently.
2. The issue reported on GitHub highlights the need for the `table_exists` function to be case-insensitive.
3. The failing tests demonstrate the failure to handle case-insensitive table name comparisons, leading to assertion errors due to false positives.
4. To fix the bug, the function should compare the table name in a case-insensitive manner to match the behavior of Hive, as suggested in the GitHub issue.

### Correction:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.splitlines())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout is not None
```

By converting both the `table` and each line in `stdout` to lower case, the corrected function ensures a case-insensitive comparison for table existence checks in Hive databases, addressing the reported issue.