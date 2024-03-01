### Bug Explanation
The bug in the `table_exists` function lies in the condition check of whether the `table` is found in the `stdout`. The bug is caused by not splitting the `stdout` properly to check for the presence of the `table` name in the output. Instead, the buggy function directly checks whether the entire `table` name is present in the `stdout`, leading to incorrect results.

### Bug Fix Strategy
To fix the bug:
1. Split the `stdout` by newline characters to separate the lines properly.
2. Check if the `table` name exists in any of the lines extracted from `stdout`.

### Corrected Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
``` 

By splitting the `stdout` by newline characters and then checking if the `table` name exists in any of the lines, the code will now properly determine the existence of the table in the Hive database.