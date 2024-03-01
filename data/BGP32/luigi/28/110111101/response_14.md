### Bug Explanation
The bug in the `table_exists` function lies in the condition where it checks if `stdout` is non-empty to determine if the table exists. Specifically, in the first case, when `stdout` is equal to `'OK\nmytable'`, the function incorrectly returns `True` because it looks for an exact match of `table` in `stdout` without considering the delimiters. This results in failing tests where the expected outcome differs from the actual return value.

### Bug Fix Strategy
To fix the bug, we need to modify the condition checking in the `table_exists` function. Instead of a simple string match, we should split `stdout` by line breaks and check if `table` exists in any of those lines. This modification will allow for a more robust check and ensure that the function behaves correctly in all cases.

### Corrected Function
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """
    
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table in stdout.split('\n')
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                       (%s)""" % (database, table, self.partition_spec(partition)))
            return bool(stdout)
``` 

By implementing the above corrections, the `table_exists` function will successfully pass the failing tests and provide the expected outcomes across different scenarios.