### Bug Explanation
The bug in the `table_exists` function lies in the conditional check for the `stdout` variable when a partition is provided. The function is returning `True` or `False` based on whether `stdout` is empty or not, which is incorrect. The expected behavior should be to check if the partition exists in the stdout output.

### Bug Fix Strategy
To fix the bug, we need to modify the conditional check for the stdout variable when a partition is provided. We should check if the specific partition exists in the stdout output by parsing the partition_spec.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd(
            'use {0}; show partitions {1}.{2}'.format(database, table, self.partition_spec(partition)))
        if stdout:
            return True
        else:
            return False
```