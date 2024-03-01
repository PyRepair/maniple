### Bug Explanation
The bug in the `table_exists` function lies in how the function checks for the existence of a table. In the `if partition is None` block, the function checks if the table name exists in the output from running the `show tables` command. However, in the `else` block, when a partition is specified, the function checks if the output from `show partitions` is not empty instead of checking for the existence of the partition.

### Bug Fix Strategy
1. Modify the `if partition is None` block to correctly handle the case where a partition is specified.
2. Update the logic in the `else` block to properly check for the existence of the specified partition.

### Corrected Version
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd("""
                use {0};
                show partitions {1} partition ({2});
            """.format(database, table, self.partition_spec(partition)))

            return bool(stdout.strip())  # Check if the partition information is returned
```

By making these changes, the `table_exists` function should now correctly determine if a table or partition exists in the specified database.