### Bug Explanation:
The bug in the `table_exists` function lies in the conditional check for the presence of the `table` in the `stdout`. The current implementation checks if `stdout` is truthy and if `table` is in `stdout`, but this logic is flawed because when `stdout` is non-empty, it will always be considered truthy, regardless of whether `table` is actually in `stdout`.

### Bug Fix Strategy:
To fix the bug, we need to update the conditional check so that it explicitly checks if `table` is in `stdout`.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return table in stdout
```