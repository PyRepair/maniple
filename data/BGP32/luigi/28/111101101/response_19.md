### Bug Explanation
The bug in the `table_exists` function is due to the way the stdout is checked to determine if the table exists. In the first part of the function, if `partition` is None, the function checks if the table name is present in the `stdout` from the `run_hive_cmd` function. However, in the second part where a partition is specified, the function returns `True` if `stdout` is not empty, regardless of the actual content of `stdout`. This inconsistency causes the tests to fail and leads to incorrect logic.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function checks the correct conditions for both cases where there is a partition specified and where there is no partition specified. We need to check if the table name exists in `stdout` for both cases.

### Corrected Code
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        partition_string = self.partition_spec(partition) if callable(partition) else partition
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, partition_string))
        
        return stdout and table in stdout
```

By modifying the function to check if the table name is present in `stdout` for both cases, we ensure consistent logic and fix the bug that was causing the failing tests.