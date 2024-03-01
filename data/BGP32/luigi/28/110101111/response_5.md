The buggy function `table_exists` in the `HiveCommandClient` class has a bug related to case sensitivity when checking for table existence. The function should be case insensitive when comparing the table name with the output from Hive.

### Bug Cause:
The bug is caused by the function not considering case sensitivity when comparing the table name with the output from Hive. As a result, tests fail when the table names are in different cases.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the function to convert both the table name and the output from Hive to the same case (e.g., lowercase) for comparison to make it case insensitive.

### Corrected Version of the `table_exists` function:
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

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

By converting both the table name and the output to lowercase before comparison, the corrected function should now pass the failing tests and make the table existence check case insensitive as requested in the GitHub issue.