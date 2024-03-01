### Analysis:
1. The buggy function `table_exists` in the `HiveCommandClient` class of `luigi.contrib.hive` module is using the `run_hive_cmd` function to execute hive commands.
2. The function checks if a table exists in a given database. If a partition is provided, it also checks if the specified partition exists.
3. The bug appears to be related to the condition checks in the function causing the incorrect return values.

### Bug:
The bug in the `table_exists` function causes incorrect return values due to faulty condition checks when processing the output of hive commands.

### Cause:
1. When running hive commands and checking the output, the condition `return stdout and table in stdout` might cause issues with empty strings.
2. The condition check for the partition also seems to cause incorrect logic and return values.

### Strategy for Fixing the Bug:
1. Handle the case of empty stdout in the `table_exists` function.
2. Verify the condition check for partitions to correctly determine if a partition exists.

### Corrected Version of the `table_exists` function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table in stdout.split()
    else:
        partition_str = ', '.join(['{0}={1}'.format(k, v) for k,v in partition.items()])
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, partition_str))

        return table in stdout
```

By modifying the condition check for both the table existence and partition existence, we ensure that the correct logic is applied. Additionally, splitting the output of `run_hive_cmd` ensures that an empty string does not lead to false positives.