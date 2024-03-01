### Bug Explanation:
The buggy function `table_exists` has a bug in the logic where it checks for table existence in different cases. The bug occurs in the return statement when checking if the table is in the output received from the `run_hive_cmd` function. The current implementation only checks for exact matches of the table name which causes the test cases to fail when the case sensitivity of the table name changes.

### Bug Fix Strategy:
To fix the bug, we need to make the table name comparison case-insensitive. This can be achieved by converting both the table name and the output from `run_hive_cmd` to lowercase before comparison.

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

By converting both the table name and the output to lowercase before comparison, the corrected function will pass the failing test cases and provide the expected behavior of a case-insensitive comparison for table existence check.