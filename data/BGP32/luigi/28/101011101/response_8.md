### Bug Explanation
The bug in the `table_exists` function is related to the way it checks for the existence of a table. In the `if partition is None` condition, the function tries to match the table name directly in the output returned by the `run_hive_cmd` function. However, in the case where the table name is part of a larger output, such as `OK\nmytable`, the function fails to correctly identify the table.

### Bug Location
The bug stems from the comparison operation `table in stdout` assuming that the table name is the only contents of `stdout`. If the table name is part of a larger string, the comparison fails.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the way the function checks for the existence of the table. Instead of a direct comparison, we should split the output and then check if the table name is present on a separate line.

### Corrected Version of the Function
```python
# Corrected version of the buggy function
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
    
        return True if table in stdout.split('\n') else False
``` 

In the corrected version, the `stdout` is split by `\n` before checking for the presence of the table name. This ensures that each line in the output is considered separately, allowing the function to correctly identify the existence of the table even within a larger output string.