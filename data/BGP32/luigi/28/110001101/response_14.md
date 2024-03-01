### Bug Explanation
The bug in the `table_exists` function arises from the condition where it checks if the `stdout` is empty to determine if a table exists or not. In the current implementation, the function returns `stdout and table in stdout`, which is incorrect. 
- In Case 1 and Case 3, the function incorrectly returns `True` when the table exists and `stdout` is not empty, leading to incorrect results. 
- In Case 2 and Case 4, the function incorrectly returns `False` when the table exists and `stdout` contains the table name, resulting in incorrect behavior.

### Bug Fix Strategy
To fix the bug, we need to modify how the function determines if a table exists. We should check if the table name is present in the output of the `show tables` command in Hive.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        return stdout and table.lower() in map(str.lower, stdout.split())
  
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        if stdout:
            return True
        else:
            return False
```