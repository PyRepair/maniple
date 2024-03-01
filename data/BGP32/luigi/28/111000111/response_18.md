## Analysis
1. The buggy function `table_exists` in the `HiveCommandClient` class uses the `run_hive_cmd` function to query for table existence in a Hive database.
2. The bug arises from the comparison of the table name in a case-sensitive manner, leading to failures when dealing with case variations.
3. The GitHub issue highlights the need to make `table_exists` case-insensitive to handle table name comparisons more effectively.
4. To fix the bug, we should convert both the table name and the output from `run_hive_cmd` to lowercase for a case-insensitive comparison.

## Bug Fix
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

By converting both `table` and `stdout` to lowercase before the comparison, we ensure a case-insensitive check for table existence. This modification aligns with the suggested fix in the GitHub issue (#896) and addresses the bug effectively.