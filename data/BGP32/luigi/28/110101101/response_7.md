### Cause of the bug
The bug in the `table_exists` function arises from the incorrect comparison of the table name in the stdout returned from the `run_hive_cmd` function. The function incorrectly checks if the table name is exactly equal to the stdout string instead of searching for the table name within the stdout string.

### Strategy for fixing the bug
To fix the bug, we need to modify the comparison in the function to check if the table name is contained within the stdout string instead of being an exact match.

### Corrected version of the function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        partition_spec = self.partition_spec(partition)
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, partition_spec))
    
        return bool(stdout)
```

In the corrected version:
- We check if the `table` is contained in the `stdout` string using `table in stdout`.
- We correctly construct the `run_hive_cmd` call with proper formatting.
- We make use of the `partition_spec` returned from the function.
- We return `True` if the `stdout` is truthy, indicating the table exists, otherwise return `False`.

This corrected version should pass the failing test cases provided.