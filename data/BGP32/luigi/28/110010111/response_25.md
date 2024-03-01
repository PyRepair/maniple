### Analysis:
1. The buggy function `table_exists()` is supposed to check if a given table exists in a specified Hive database using the `run_hive_cmd` function.
2. The issue reported on GitHub (#896) indicates that the function should be case-insensitive when checking table existence.
3. The bug arises from the function not handling case sensitivity properly when comparing the table name with the output from `run_hive_cmd`.
4. To fix the bug, we need to ensure that the comparison between the table name and the output from Hive is case-insensitive.

### Bug Cause:
The bug is caused by the function not considering case sensitivity when comparing the table name with the output from Hive. If the table name and the output have different case formats, the comparison fails.

### Fix Strategy:
1. Modify the function to convert both the table name and the output to lowercase before comparison.
2. Use the `lower()` function to ensure case-insensitive comparison.

### Corrected Function:
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

By converting both the table name and the output to lowercase before comparison, the corrected function will now be case-insensitive, resolving the bug and passing the failing tests.