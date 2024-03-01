## Analysis:
1. The buggy function `table_exists` checks if a table exists in the specified database in Hive.
2. The function uses the `run_hive_cmd` function to execute Hive commands.
3. There are potential errors in the way the Hive command is constructed and executed, especially when dealing with partitions.
4. The bug seems to be related to the way the Hive command is built when a `partition` is provided.

## Bug Cause:
The bug occurs when the `table_exists` function constructs the Hive command to check for existence of a partitioned table. The way the command is built for partitions using `self.partition_spec(partition)` method may not be correct, leading to incorrect results. This can cause the function to incorrectly determine the existence of the table.

## Fix Strategy:
1. Ensure that the Hive command is properly constructed when checking for partitioned tables.
2. Validate the Hive command format being used to show partitions and check for existence of the table.
3. Handle any edge cases related to partition specification.

## Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        partition_cmd = ' '.join(self.partition_spec(partition))  # Construct the partition command
        
        cmd = """use {0}; show partitions {1} partition ({2})""".format(database, table, partition_cmd)
        
        stdout = run_hive_cmd(cmd)
    
        return stdout is not None  # Return True if stdout is not empty
```

In this corrected version:
- The partition command is constructed using the result of `self.partition_spec(partition)` and properly formatted.
- The constructed Hive command is then executed using `run_hive_cmd`.
- The function checks for the presence of output in `stdout` to determine the existence of the partitioned table.