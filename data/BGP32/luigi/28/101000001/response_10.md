## Analysis:
1. The `table_exists` function is supposed to check if a given table exists in the specified database, with the option to include a partition.
2. The function uses the `run_hive_cmd` function to execute Hive commands and check the output.
3. The bug might be related to the incorrect concatenation of the Hive command string when a partition is provided.
4. The bug seems to be in the string formatting when constructing the Hive command.

## Bug Cause:
The bug is caused by incorrect string formatting in the Hive command creation while handling partitions.

## Strategy for Fixing the Bug:
To fix the bug in the `table_exists` function, we need to ensure that the Hive command string is correctly formatted for both cases (with and without partition). We need to properly format the command string and handle the partition case appropriately.

## Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, self.partition_spec(partition)))
        return stdout and len(stdout.strip()) != 0
``` 

In the corrected version, the Hive command string is formatted properly for both cases. The partition information is correctly added to the Hive command when provided. Additionally, the condition for checking if the table exists has been modified to handle the stdout output more accurately.