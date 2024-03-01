### Explanation of the Bug:
The bug in the `table_exists` function is due to the case sensitivity issue when comparing the table name with the output from the Hive command. Hive is case insensitive and returns table names in lowercase, leading to test failures when comparing with the original table name.

### Bug Fix Strategy:
To fix the bug, we need to convert both the table name and the output from the Hive command to lowercase before comparison. This will ensure a case-insensitive check and resolve the failing tests.

### Corrected Version of the Function:
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

By converting both the `table` and `stdout` to lowercase before comparison, the corrected function will now pass the failing tests and resolve the case sensitivity issue as reported in the GitHub issue.