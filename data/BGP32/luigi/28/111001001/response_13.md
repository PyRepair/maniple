### Bug Explanation
The bug in the `table_exists` function arises from the way the function checks whether a table exists in a database. When `partition` is provided, the function constructs a query incorrectly, which leads to incorrect processing of the `stdout` results.

### Bug Fix Strategy
To fix the bug, the function should construct the query correctly when a partition is provided, ensuring that it matches the expected syntax for Hive commands.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd('''use {0}; show partitions {1} partition
                            ({2});'''.format(database, table, self.partition_spec(partition)))

        return bool(stdout)
```