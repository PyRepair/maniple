### Bug Explanation
The bug in the `table_exists` function is in the comparison of the `table` variable with the `stdout` variable. In Case 2 and Case 4, even though the table name is present in the `stdout` variable, the comparison is failing because of a case mismatch.

### Bug Fix Strategy
To fix this bug, we need to make the comparison case-insensitive by converting both the `table` and `stdout` variables to lowercase before comparison.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table.lower()))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table.lower(), self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

In the corrected version, both `table` and `stdout` are converted to lowercase using the `lower()` function before comparison, making it case-insensitive. This should resolve the bug and ensure that the function works correctly in all cases.