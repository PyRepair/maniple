### Bug Explanation
The bug in the `table_exists` function arises from how the expected output is being handled. The function checks if the `stdout` variable contains the table name but does not consider the format of the output accurately. In the failing test cases, the comparison logic fails because the `stdout` variable contains additional information besides just the table name, causing the check to return incorrect results.

### Bug Fix Strategy
To fix the bug, we need to refine the comparison logic to handle the different formats of the `stdout` variable properly. We should ensure that the comparison is strict and accurate based on the expected format.

### Corrected Version of the Function
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

By splitting the `stdout` variable on newline characters, we can accurately extract the table names. This modification ensures that the comparison between the expected table name and the retrieved table names from the output is correctly handled.