### Analysis:
1. The `table_exists` function checks if a table exists in a given database by running a Hive command using `run_hive_cmd` function.
2. In the first case, when `partition` is None, the function runs a Hive command to check if the table exists.
3. In the second case, when `partition` is not None, the function constructs a Hive command with the partition information.
4. The issue arises when the function tries to check if the table exists based on the output of the Hive command. The function expects the table name to be directly present in the output, but sometimes it comes with other information like partition spec, leading to incorrect results.

### Bug:
The bug occurs when the function incorrectly checks if the table is present in the output of the Hive command. The function expects a direct match between the table name and the output, but due to the additional partition information present in the output, the comparison fails.

### Fix:
To fix the bug, we need to modify the logic of how the function checks if the table exists. Instead of searching for an exact match in the output, we can split the output by newlines and check each line for the table name separately. This way, we can accurately determine if the table exists, even if partition information is included in the output.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        if stdout:
            return any(t.strip() == table for t in stdout.split("\n"))
        else:
            return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
        if stdout:
            return any(t.strip() == table for t in stdout.split("\n"))
        else:
            return False
``` 

By splitting the output and comparing each line to the table name, we ensure that the function correctly identifies if the table exists without being affected by other information in the output.