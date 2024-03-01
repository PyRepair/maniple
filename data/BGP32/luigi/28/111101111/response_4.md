### Cause of the bug:
The bug in the `table_exists` function arises from the fact that when checking if a table exists, the comparison between the table name and the tables listed in the output of the `run_hive_cmd` function is case-sensitive. This discrepancy leads to the failing test cases where the function should correctly identify the table existence, regardless of the case of the table name.

### Strategy for fixing the bug:
To fix the bug, we need to ensure that the comparison between the table name and the tables listed in the `stdout` output is case-insensitive. This can be achieved by converting both `table` and `stdout` to lowercase before comparing them.

### Corrected version of the buggy function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("use %s; show partitions %s partition (%s)" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By converting both the `table` and `stdout` to lowercase before comparison, the corrected version of the function ensures that the table existence check is case-insensitive. This change aligns with the GitHub issue raised (#896) and addresses the failing test cases related to case sensitivity.