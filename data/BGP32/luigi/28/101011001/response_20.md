### Bug Explanation:
The bug in the `table_exists` function lies in the way the function checks for the existence of the specified table. When the function receives a `partition` parameter, it uses the `run_hive_cmd` function to check for partitions that match the specified partition. However, it does not properly handle the case where the command returns an empty string. This results in the function returning `True` even when the table does not actually exist.

### Bug Fix:
To fix the bug, we need to modify the logic in the `table_exists` function to handle the case where the command output is empty. We should check if the `stdout` variable is not empty before returning `True`. If the `stdout` is empty, we should return `False`.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
    
        return bool(stdout)
```

By modifying the return statement in the `table_exists` function to `return bool(stdout)`, we ensure that the function only returns `True` if the `stdout` variable is not empty, indicating that the table exists in the specified database and partition. This fix addresses the bug and should now pass the failing tests.