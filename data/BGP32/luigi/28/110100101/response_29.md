### Bug Explanation:
The bug in the `table_exists` function arises from the condition checks on the `stdout`. In the first condition, the function checks `return stdout and table in stdout`, which will only return `True` if both `stdout` is not empty and `table` is present in `stdout`. However, in the second condition, the function only checks if `stdout` exists without validating its content, leading to incorrect results.

### Bug Fix Strategy:
To fix the bug, we need to modify the second condition to properly check if the `table` is present in the `stdout` for the case when `partition` is not None. We should ensure consistency in the condition checks for both cases.

### Corrected Version of the Function:
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

By fixing the condition in the `else` block to include a check for `table in stdout`, we ensure that the function correctly validates the existence of the table in the output. This correction will address the bug and make the function behave as expected for all test cases.