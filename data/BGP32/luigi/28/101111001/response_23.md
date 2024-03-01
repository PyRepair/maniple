### Bug Explanation
The bug in the `table_exists` function lies in the condition where it checks if the table name is present in the `stdout` output. The function incorrectly checks if `stdout` exists and if the table is in `stdout`. This leads to incorrect evaluation of the `stdout` content, causing the test cases to fail.

### Bug Fix Strategy
To fix the bug, we need to update the condition where we are checking if the table is in the `stdout` output. We need to properly split and process the `stdout` output to correctly determine if the table exists.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout.strip().split("\n")
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
    
        return bool(stdout)
``` 

By splitting the `stdout` output by newline character and checking if the table name is in the resulting list, we ensure that the table existence check is correctly performed. This corrected version should now pass the failing test cases.