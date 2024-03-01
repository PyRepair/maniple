### Bug Explanation:
The bug in the `table_exists` function occurs due to how the function checks for the table existence in Hive. When checking for the table existence with partitions, the function constructs the Hive command incorrectly, leading to failures in identifying the table.

In the case where partitions are involved, the function builds the Hive command with the table name and the partition specification but fails to handle newlines properly in the `stdout` variable. This results in the function incorrectly determining the table's existence based on the output from the Hive command.

### Bug Fix Strategy:
To fix this bug, we need to ensure that the `stdout` variable is properly parsed when partitions are involved. Specifically, we should split the `stdout` into individual lines and check if the table exists in any of those lines.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("use %s; show partitions %s partition (%s)" % (database, table, self.partition_spec(partition)))
        
        if stdout:
            return True
        else:
            return False
``` 

With this corrected version, the function should now effectively check for the existence of the table, including cases where partitions are involved.