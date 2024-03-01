### Bug Explanation
The bug in the `table_exists` function arises from the handling of the `partition` parameter. In the implemented code, when `partition` is not None, the function constructs a command using the `partition_spec` and checks if the output is not empty to return True. However, the logical error occurs as the function always returns True when `stdout` is not empty, regardless of the actual content of the output.

### Bug Fix Strategy
To fix the bug, we need to modify the logic within the function to correctly handle the case when a partition is provided. The function should check if the partition is present in the output `stdout` instead of just checking for non-empty output.

### Corrected Function
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
            partition_str = self.partition_spec(partition)
            stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, partition_str))
    
            return partition_str in stdout
```

By modifying the return logic in the function to check if the partition string is present in the `stdout`, we ensure that the function correctly verifies the existence of the table with a specific partition. This corrected version should pass the failing test cases and produce the expected output.