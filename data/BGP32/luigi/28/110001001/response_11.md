### Bug Explanation
The bug in the `table_exists` function is due to how the function checks for the existence of a table. In the first case, when checking for a table without partitions, the function only checks if the table name is directly in the output from the Hive command. However, in the second case, when checking for a table with partitions, the function does not account for the fact that the partition names might be included in the output as well, leading to incorrect results.

### Bug Fix
To fix the bug, we need to modify the function to account for the different scenarios when checking for table existence with or without partitions. The function should properly parse the output of the Hive command to determine if the table exists or not.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        partition_spec = self.partition_spec(partition)
        stdout = run_hive_cmd("""use {0}; show partitions {1}.{2} partition
                            ({3})""".format(database, database, table, partition_spec))
        return stdout and partition_spec in stdout
``` 

By properly constructing the Hive command and checking if the table and partition exist in the stdout, the corrected function should now return the correct results for both cases provided.