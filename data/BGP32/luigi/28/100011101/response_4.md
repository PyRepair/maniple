### Bug Explanation
The bug in the provided function stems from the comparison in the `if` conditions. In the first case, the function is checking if the `stdout` variable is not empty, but the condition used is `return stdout and table in stdout`, which might not work as expected if `stdout` contains any other values than the table name. This leads to unexpected behavior in certain cases.

### Bug Fix Strategy
To fix the bug, we should modify the conditions to ensure correct comparison. We should check if the table name is present in the `stdout` output for the first case, and for the second case, just check if the `stdout` is not empty.

### Updated Function
Here is the corrected version of the function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout if stdout else False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By updating the conditions to check for the presence of the table name and the existence of output in a more clear way, the corrected function should now pass the failing tests and provide the expected behavior.