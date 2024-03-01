### Bug Explanation:
The bug in the `table_exists` function lies in the conditional check for the `stdout` variable. In the first case where `partition` is `None`, the function incorrectly checks if `stdout` is not empty and if the `table` is in `stdout`. The logical operator `and` should be replaced with `in` to correctly check if the `table` is in `stdout`. 

In the case where `partition` is not `None`, the function incorrectly returns `True` if `stdout` is non-empty, without checking if the `table` is in `stdout`. This leads to a false positive result.

### Bug Fix Strategy:
1. When `partition` is `None`, change the conditional statement to check if the `table` is in `stdout`.
2. When `partition` is not `None`, after obtaining `stdout`, check if both the `table` and the `partition` spec are in `stdout`.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout and table in stdout and self.partition_spec(partition) in stdout
```