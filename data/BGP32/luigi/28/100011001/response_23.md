### Bug Explanation
The bug in the `table_exists` function lies in the conditional check for returning `True` or `False`. In the first case, when `partition` is None, the function checks if the `table` exists in the output of the `run_hive_cmd` function. However, in the second case when `partition` is not None, the function checks if the output of the `run_hive_cmd` function exists, which always evaluates to `True` even if the table does not exist.

### Bug Fix
To fix the bug, we need to modify the conditional checks in the `table_exists` function to correctly handle both cases when a partition is specified and when it is not.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return "OK" in stdout
``` 

By returning `True` if "OK" is in the `stdout`, we ensure that the function correctly identifies the existence of the table, whether a partition is specified or not. This modification addresses the bug and should make the tests pass successfully.