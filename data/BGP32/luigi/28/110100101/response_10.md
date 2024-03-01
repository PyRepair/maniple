### Bug Explanation
The current `table_exists` function in the `HiveCommandClient` class fails to correctly check if a table exists in the specified database. The bug occurs because the function incorrectly interprets the output of the `run_hive_cmd` function and does not properly handle the partitioned table cases.

In the first part of the function, when partition is `None`, the function expects the `stdout` response to contain a table name if it exists. However, it checks `table in stdout`, which does not account for any additional characters or formatting that might be present in the stdout.

In the second part, when a partition is specified, the function constructs a command to show partitions that match a specific partition specification, however, it does not handle the output correctly.

### Bug Fix Strategy
1. Modify the first part of the function to properly handle the stdout response by splitting it into separate lines and then checking if the table name is present. This way, we can ensure that we are correctly interpreting the output.
2. Update the second part to properly handle the partitioned tables by using the correct command and checking for the existence of the specified partition.

### Corrected Function

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table)).split("\n")
    
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition))).split("\n")
    
            return any(partition in line for line in stdout)
```

After updating the function as described above, it should now correctly handle both non-partitioned and partitioned table cases and pass all the provided test cases.