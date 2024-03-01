## Analysis:
The buggy function `table_exists` is not correctly handling the `run_hive_cmd` function calls for checking table existence with or without partitions. The issue lies in how the output of `run_hive_cmd` is being checked to determine if the table exists. The function should return `True` when the table is found in the output, and `False` otherwise.

## Error Location:
The bug is primarily in the conditionals where `stdout` is being checked. The logic in the if statements is reversed, causing the function to return the wrong values.

## Bug Cause:
The bug occurs because the logic in the conditional statements for checking the existence of the table in the `stdout` of `run_hive_cmd` is inverted. The function is returning `True` if the table is not found and `False` if it is found.

## Strategy to Fix the Bug:
To fix the bug, we need to correct the conditional expressions inside the `table_exists` function to return `True` when the `table` is found in the `stdout` of `run_hive_cmd`. We should also maintain the current logic for handling partitions.

## Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
    
        return stdout and table in stdout
``` 

By modifying the return statements to check if `table in stdout` and returning the result, we correct the bug. This way, the corrected function should now pass the failing test cases provided.