### Bug Explanation:
The bug in the `table_exists` function arises from the way the `run_hive_cmd` function is called with different queries depending on whether a partition is provided. In the cases where the partition is not None, the query constructed is incorrect, resulting in unexpected stdout values and leading to incorrect return values.

### Bug Fix Strategy:
To fix the bug in the `table_exists` function, we need to ensure that the query construction for the partition case is correct. This involves properly formatting the query string based on the partition information provided.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        partition_string = ','.join(['{key}={value}'.format(key=k, value=v) for k, v in partition.items()])
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, partition_string))

        if stdout:
            return True
        else:
            return False
```

With this corrected version of the function, the queries constructed for the partition case will be formed correctly, and the function should now pass the failing tests with the expected input/output values.