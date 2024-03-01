### Bug Explanation
The bug in the `table_exists` function arises from how the condition for checking if the table exists is implemented. The function is returning `True` when the table is found in the stdout output, which is incorrect. The expected behavior should be to return `True` only if the table exists, but the current implementation returns `True` if the table name is found in the output string, regardless of whether the table actually exists or not.

### Bug Fix Strategy
To fix this bug, we need to modify the logic in the `table_exists` function to accurately determine if the table exists in the database based on the stdout output from the `run_hive_cmd` function.

### Corrected Version
```python
class HiveCommandClient(HiveClient):
    def partition_spec(self, partition):
        # Implement the logic for partition_spec if required

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables "{1}";'.format(database, table))
    
            return stdout.strip() == table
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
    
            return bool(stdout)
```

In the corrected version, the `table_exists` function now checks if the table name is exactly matched in the stdout output for the first case (when `partition` is None). For the second case (when `partition` is not None), the function simply checks if the `stdout` has any content which indicates that the command was successful. This revised logic will fix the bug and ensure that the `table_exists` function behaves as expected based on the input parameters and stdout output.