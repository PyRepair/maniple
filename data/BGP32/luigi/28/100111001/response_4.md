### Bug Explanation
The bug in the `table_exists` function is due to the incorrect logic when checking if a table exists in the database. The function is returning `True` when it should be returning `False`, and vice versa, based on the presence of the table in the output of the `run_hive_cmd` function.

In the buggy function:
1. In the `if partition is None:` block, the function checks if the `table` is in the `stdout` to determine if the table exists. However, it should return `True` when the `table` is in `stdout`, not when it's not in `stdout`.
2. In the `else:` block, the function checks if `stdout` exists to determine if a table exists with a partition. It should return `True` when stdout exists, indicating the table with the partition exists.

### Bug Fix Strategy
To fix the bug, we need to adjust the `if` conditions to return the correct values based on whether the table is present in the output or not.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        if stdout:
            return True
        else:
            return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
        
        if stdout:
            return True
        else:
            return False
``` 

By making the above corrections to the `table_exists` function, it should now correctly determine if a table exists in the database, passing the failing tests.