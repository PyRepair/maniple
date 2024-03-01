### Bug Explanation
The bug in the `table_exists` function is due to the comparison between the `table` and the `stdout` variable in the `if` condition. The bug arises from the fact that the comparison is case-sensitive, meaning that if the `table` name is provided in a different case than the `stdout` output, the comparison will fail.

### Bug Fix Strategy
To fix the bug, we need to make the comparison case-insensitive. One way to achieve this is by converting both the `table` and `stdout` values to lowercase before comparison.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

This corrected version of the function ensures that the comparison between the `table` name and the `stdout` output is case-insensitive, fixing the bug.