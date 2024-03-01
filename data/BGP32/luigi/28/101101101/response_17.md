### Bug Explanation
The bug in the `table_exists` function lies in the conditional check for the existence of the table in the `stdout` variable. The function checks if the `table` is in the `stdout`, but it does not handle cases where there might be extra whitespace or newline characters in the `stdout` output. This leads to the incorrect evaluation of whether the table exists or not.

### Bug Fix Strategy
To fix the bug, we need to modify the conditional check to properly handle cases where there might be extra whitespace or newline characters in the `stdout` output. We should strip the `stdout` before checking if the `table` exists in it.

### Corrected Function
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.strip()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
```

By adding the `strip()` method to the `stdout` variable before checking if the `table` is in it, we ensure that any leading or trailing whitespace or newline characters are removed, and the presence of the table is accurately evaluated.