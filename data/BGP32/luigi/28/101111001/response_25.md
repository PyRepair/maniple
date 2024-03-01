### Bug Explanation
The bug in the `table_exists` function arises from the condition used to determine if a table exists. In the buggy function, the condition checks if the table is in the output of the `run_hive_cmd` function. However, the current implementation of the condition is flawed, leading to incorrect results and failing tests.

### Bug Location
The issue lies in how the function checks for the presence of the table name in the output of the `run_hive_cmd` function.

### Bug Cause
1. When the output `stdout` from `run_hive_cmd` is equal to "OK", the function returns `True`. This would be incorrect as it should only return `True` if the table is listed in the output.

2. In the case where the output `stdout` contains the table name, the function correctly returns `True`. 

3. Lastly, the function does not handle empty output correctly and always returns `False`.

### Bug Fix Strategy
To fix the bug, we need to update the condition used to determine if the table exists. The condition should check if the table name is present in the output of the `run_hive_cmd` function. Additionally, we need to handle cases where the output is empty to return `False`.

### Corrected Function
```python
class HiveCommandClient(HiveClient):
    
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            partition_str = self.partition_spec(partition)
            stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, partition_str))
    
            return table in stdout.splitlines()
```

After making the above correction, the `table_exists` function should now correctly check if a table exists in Hive and pass the failing tests.