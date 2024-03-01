### Bug Explanation
The bug in the `table_exists` function is due to the incorrect comparison logic. In the `table_exists` function, when checking for the existence of a table without a partition, it checks if the `table` is in the `stdout` directly. However, when checking for the existence of a table with a partition, it simply checks if `stdout` is not empty, which always evaluates to `True` regardless of the actual content of `stdout`.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function correctly checks whether the table exists in the output `stdout`, both for tables with and without partitions. We can achieve this by modifying the comparison logic based on the actual data in `stdout`.

### Corrected Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd(
            'use {0}; show partitions {1} partition ({2});'.format(database, table, self.partition_spec(partition))
        )
        return stdout.strip() == table
```

After implementing this corrected code, the function should now correctly determine whether a table exists in Hive based on the provided parameters and the output from the command. This fix should address the failing tests and match the expected input/output values. It now correctly handles both cases where `partition` is `None` and when it is specified.