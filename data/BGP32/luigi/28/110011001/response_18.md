### Bug Explanation
The bug in the `table_exists` function lies in the conditional statements used to determine whether a table exists or not. In the first block of code, when `partition` is `None`, the function checks if the `table` is in the output of the `run_hive_cmd` function. However, in the second block of code, when `partition` is not `None`, the function checks if the output obtained from the `run_hive_cmd` function returns anything at all, regardless of the content.

The issue arises when the partition is not None, as it directly returns `True` if the `run_hive_cmd` function returns any output, even if it doesn't contain the specific table name.

### Fix Strategy
The function should be modified to check if the table exists in the output of the `run_hive_cmd` function when a partition is specified. This can be achieved by updating the condition in the second block of code to include checking if the table name is present in the output.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table in stdout
    else:
        partitions_output = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, self.partition_spec(partition)))

        return table in partitions_output
``` 

By updating the return statement in the else block to check if the table name is present in the output obtained from the `run_hive_cmd` function when a partition is specified, the corrected function should now pass the failing tests.