### Bug Explanation

The bug in the `table_exists` function lies in the condition checking whether the `table` is in the `stdout` string returned from the `run_hive_cmd` function. The bug arises due to how the check is performed. In one case, the function correctly checks if the `table` is in the `stdout` string, but in the other case, it only checks if `stdout` exists, leading to the wrong output. This inconsistency causes the function to fail the test cases where it is expected to return `True`.

### Bug Fix Strategy

To fix the bug, we need to ensure that the function correctly handles both cases of checking the presence of the table in the `stdout` string. The function should return `True` if the `table` is present in the `stdout` and `False` if it is not.

### Corrected Code

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout if stdout else False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        return True if stdout else False
``` 

With this correction, the function should now pass the failing test cases.