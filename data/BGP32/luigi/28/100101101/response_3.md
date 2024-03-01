### Cause of the Bug
The bug in the `table_exists` function lies in the condition checks in the if statements. The function returns `True` if `stdout` is not empty, which is incorrect. The function should return `True` only if the table exists in the output of the Hive command.

### Fixing the Bug
To fix the bug, we need to modify the condition checks in both branches of the if-else statement to properly check if the table exists in the `stdout`. We should only return `True` if the table is found in the output, otherwise return `False`.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return table in stdout.splitlines()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By modifying the condition check to specifically check if the table name exists in the `stdout` output, the function will now correctly determine if a table exists in Hive.