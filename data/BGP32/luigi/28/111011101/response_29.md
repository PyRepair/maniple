### Bug Explanation
The bug is related to how the `table_exists` function handles the partition parameter. When the partition parameter is provided, the function uses `self.partition_spec(partition)` to generate the partition specification for the Hive command. However, in the failing tests, the generated partition specification is not being handled correctly in the Hive command string, leading to incorrect results.

### Bug Fix Strategy
To fix the bug, we need to ensure that the generated partition specification is correctly formatted within the Hive command string when the partition parameter is provided. This involves properly including the partition specification in the Hive command to accurately check for the existence of the table with that specific partition.

### Corrected Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        if stdout:
            return True
        else:
            return False
    else:
        partition_str = ','.join([f"{k}='{v}'" for k, v in partition.items()])
        stdout = run_hive_cmd(f"use {database}; show partitions {table} partition ({partition_str})")

        if stdout:
            return True
        else:
            return False
``` 

### Updated Explanation
In the corrected code:
1. We properly format the partition specification in the Hive command string using the provided partition dictionary.
2. Use an f-string format to construct the Hive command when the partition parameter is not None.
3. Updated the condition to return True if stdout is not empty. This aligns with the behavior typically expected in such checks.
4. The corrected function should now handle the partition correctly and pass the failing tests by checking for the existence of tables with the specified partitions.