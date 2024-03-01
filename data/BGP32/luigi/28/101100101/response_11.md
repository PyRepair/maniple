### Bug Explanation
The bug in the `table_exists` function lies in the condition where the function checks if the table name exists in the output of the `run_hive_cmd` function. In the first conditional branch, the function checks if the table name is present in the `stdout` variable directly. However, in the second conditional branch where partition information is involved, the function checks if `stdout` is not empty, which may lead to unexpected results.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function correctly handles the case where there are partitions involved. We should modify the second conditional branch to check if the table name is present in the `stdout` variable instead of just checking if `stdout` is not empty.

### Corrected Version
```python
class HiveCommandClient(HiveClient):

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            spec = self.partition_spec(partition)
            stdout = run_hive_cmd('''use {0}; show partitions {1} partition ({2})'''.
                                  format(database, table, spec))
    
            return stdout and table in stdout
```

After making these changes, the `table_exists` function should now pass all the provided test cases and handle both regular table existence checks as well as checks with partitions involved.