### Analysis:
1. The function `table_exists` is intended to check if a table exists in a given database in Hive.
2. The function checks if the table exists by running Hive commands.
3. There are two branches in the function: one for when `partition` is `None` and the other for when it is not `None`. 
4. The bug seems to be in the second branch where the Hive command is not correctly built to check for table existence with specific partitions.
5. The function currently returns `True` when stdout is not empty, which is incorrect.

### Bug:
In the else branch of the `table_exists` function, the Hive command to check for table existence with specific partitions is not correctly formatted. Additionally, the function always returns based on the presence of stdout rather than checking for the specific table.

### Fix:
1. In the else branch, correct the Hive command to properly check for table existence with specific partitions.
2. Modify the return statement to check if the specific table is present in the stdout when partition is provided.

### Corrected Code:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table in stdout
    else:
        cmd = 'use {0}; show partitions {1} partition ({2});'.format(database, table, self.partition_spec(partition))
        stdout = run_hive_cmd(cmd)
        
        return stdout and partition in stdout
``` 

By correcting the Hive command and the return statement, the function now correctly checks for table existence with specific partitions in the Hive database.