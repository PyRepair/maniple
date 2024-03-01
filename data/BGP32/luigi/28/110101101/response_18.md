### Bug Explanation
The buggy function `table_exists` in the `HiveCommandClient` class is not handling the case-sensitive comparison of table names correctly. When checking if a table exists, it is comparing the table name from the output of the Hive command without considering the case.

In Case 1 and Case 2, the function fails to recognize the table because it is considering the case of the table name. Specifically, in Case 2, the table name 'MyTable' is treated differently than 'mytable'.

### Bug Fix Strategy
To fix this bug, we need to modify the function to perform a case-insensitive comparison when checking if the table exists.

### Corrected Function
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

By converting both the table name and the output to lowercase before comparison, this corrected function will pass the failing test cases, addressing the case-sensitivity issue.