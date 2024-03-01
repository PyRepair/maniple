### Bug Explanation
The bug in the `table_exists` function lies in the condition where it checks for the presence of the table in the output obtained from running a Hive command. The current implementation checks if the table name is exactly equal to the entire output string, which can lead to incorrect results. In Cases 1 and 3, the function incorrectly returns `False` even though the table exists because the output string includes additional information (e.g., 'OK\nmytable').

### Bug Fix Strategy
To fix the bug, we need to modify the condition to check if the table name is present in the output string instead of an exact match. This will ensure that the function correctly identifies the table's existence in the Hive output.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

By making the simple adjustment of checking if the table name is in the output rather than a direct comparison, the corrected version of the function will now pass the failing tests.