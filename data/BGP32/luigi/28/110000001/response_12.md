## Analysis:
- The buggy function `table_exists` is checking if a table exists in a given database with an optional partition.
- The function uses the `run_hive_cmd` function to execute Hive commands and check the output.
- The bug lies in the handling of the `partition` parameter when checking for table existence.

## Error Location:
- The bug occurs in the `else` block of the `table_exists` function when constructing the Hive command for checking partitions.

## Cause of the Bug:
- The bug is caused by incorrectly constructing the Hive command in the `else` block when checking for partitions. The partition specification is not correctly passed in the command.

## Fixing Strategy:
- Update the Hive command generation in the `else` block to include the correct partition specification.
- Ensure that the Hive command for checking table existence is properly generated for both cases with and without partitions.

## Corrected Version:
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
            partition_spec = self.partition_spec(partition)
            stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, partition_spec))
            return bool(stdout)
```