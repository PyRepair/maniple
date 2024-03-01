### Bug explanation
The bug in the `table_exists` function occurs due to the way the `stdout` variable is being checked to determine if the table exists. The function checks if the `stdout` variable is not empty to return `True`, but in some cases, even if the table exists, the check fails due to incorrect comparison.

### Bug fix strategy
To fix the bug, we should modify the check for `stdout` to properly verify if the table is present in the `stdout` output. This can be done by checking if the table name is a substring of the `stdout` output.

### Corrected function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
    
        return table in stdout
``` 

By modifying the return statements in both cases to check if the `table` string is present in the `stdout`, we ensure that the function correctly determines if the table exists.