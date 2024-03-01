### Bug Explanation
The bug in the `table_exists` function is due to the way the function checks if the table exists in the Hive database. When no partition is specified, the function uses `show tables like` to check for the table existence, but the condition `stdout and table in stdout` is incorrect. It should be checking if the table name is present in the output `stdout` after splitting it by newlines. Similarly, when a partition is specified, the function uses `show partitions` command but fails to properly check the existence of the table.

### Bug Fixing Strategy
To fix the bug, we need to adjust the logic of how the function checks for table existence. Specifically, we need to split the `stdout` by newlines to properly parse the output and then check if the table is present in the output. We also need to adjust the logic for when a partition is specified to ensure the table existence is correctly verified.

### Corrected Function
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        return stdout and table in stdout.split('\n')
    else:
        partition_str = ', '.join(['{0}="{1}"'.format(k, v) for k, v in partition.items()])
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2})".format(database, table, partition_str))
        return bool(stdout)
``` 

By splitting the `stdout` by newlines and properly forming the partition filter conditions when necessary, the corrected function should now pass all the failing test cases and satisfy the expected input/output values.