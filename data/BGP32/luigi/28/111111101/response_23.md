### Explanation:
The bug in the `table_exists` function lies in how it handles the case when the `stdout` variable is not empty. The function checks if `stdout` is truthy, indicating that a result was received, and then checks if the `table` is in `stdout`. However, the function fails to handle cases where the `table` is a substring of another table name in the output.

### Solution:
To fix the bug, we need to modify the condition where we check if the table is in the `stdout`. Instead of directly checking for containment, we should split the lines in `stdout` and then check if `table` is equal to any of the lines. This approach ensures that we are comparing the full table name accurately.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and any(line.strip() == table for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                              (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
``` 

By making this change, the function will accurately check if the output tables match the specified table name, passing the failing tests and meeting the expected input/output values.