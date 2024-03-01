### Bug Explanation
The bug in the `table_exists` function is due to the incorrect comparison of the `stdout` value. In the `if` condition, it checks if `stdout` exists and if the `table` is in `stdout`, which is wrong. The `stdout` value can include multiple tables separated by newline characters, so we need to check if the `table` is in one of the lines of `stdout`.

### Bug Fix Strategy
To fix the bug, we need to split the `stdout` value by newline characters and then check if the `table` is in any of the lines.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By modifying the return statements to properly split the `stdout` by newline characters and check each line for the table, the corrected function should now pass the failing test cases and satisfy the expected input/output values.