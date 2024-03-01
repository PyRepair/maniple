### Bug Explanation
The bug in the `table_exists` function lies in the condition for checking if the table exists. In the case where the table name is not found in the output of the `run_hive_cmd` function, the function still returns `True` instead of `False`.

### Bug Fix Strategy
To fix the bug, we need to update the condition where we check if the table name is in the output of the `run_hive_cmd` function. If the table name is not found, we should return `False` instead of `True`.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return bool(stdout and table in stdout)  # Change made here
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
    
        return bool(stdout)
``` 

By making this change, the corrected function will now return `False` when the table name is not found in the output, and `True` when it is found, aligning with the expected behavior and passing the failing tests.