### Bug in the Buggy Function
The bug in the `table_exists` function occurs due to the comparison logic in the `if stdout:` condition. When the `stdout` variable is not empty, the function should return `True`. Still, the buggy function incorrectly checks if `stdout` itself is True instead of checking if the string `'OK\n'` (or `stdout`) contains the `table` name. This discrepancy leads to incorrect results.

### Fixing the Bug
To fix the bug, we need to modify the comparison logic in the `if stdout:` condition to check if the `table` name exists in the `stdout` string.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
    
        return stdout and table in stdout
```

By updating the return statements in both branches of the function, the corrected version now properly checks if the `table` exists in the `stdout` string, ensuring the function works as expected in all cases.