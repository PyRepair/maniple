### Bug Explanation
The buggy function `table_exists` is not correctly handling the case-insensitive search for table names. The function checks if the table name is present in the output obtained from running a Hive command. However, it does a direct string comparison which is case-sensitive, causing the tests to fail when the case of the table name is different.

### Bug Fix Strategy
To fix this bug, we need to modify the comparison of the table names to be case-insensitive. This can be achieved by converting both the table name and the output to lowercase before comparison.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table.lower()))

        return stdout and table.lower() in map(str.lower, stdout.splitlines())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By converting both the `table` and the output to lowercase before comparison, the function now handles case-insensitive checks properly and should pass the failing tests.