### Bug Analysis:
1. The `table_exists` function in the `HiveCommandClient` class is not computing the correct output based on the input parameters.
2. The bug seems to be related to how the function handles the `partition` parameter.
3. The failing test `test_table_exists` is mocking the `run_hive_cmd` function in such a way that it returns different outputs based on the input, and the `table_exists` function should return `True` if the table exists and `False` if it does not.
4. The bug can be fixed by properly formatting the `stdout` variable based on whether the `partition` parameter is provided or not.

### Bug Fix:
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, self.partition_spec(partition)))
            return bool(stdout)
```

### Updated Method:
I have corrected the formatting of the `stdout` variable based on whether the `partition` parameter is provided or not. The corrected version should now pass the failing test.