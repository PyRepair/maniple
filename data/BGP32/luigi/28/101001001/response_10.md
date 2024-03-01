### Bug Explanation
The buggy function `table_exists` is designed to check if a given table exists in a specified database. The bug arises from the comparison between the table name and the output from the `run_hive_cmd` function. In the first case, the buggy function checks if the table name is directly contained in the output, which is incorrect because the output may contain other information along with the table names.

In the second case, the buggy function splits the output by newline characters and checks if the table name is in the list of strings, leading to an incorrect check due to case sensitivity issues.

### Bug Fix
To fix this bug, we need to update the comparison logic in the buggy function. We will modify the function to split the output by newline characters and then compare the table name in a case-insensitive manner.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and any(t.lower() == table.lower() for t in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
```