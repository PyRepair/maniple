### Analysis
The buggy function `table_exists` is supposed to check if a table exists in a given database and optionally in a specific partition. The function relies on the `run_hive_cmd` function and the `partition_spec` method from the same class. The bug seems to be related to how the `run_hive_cmd` function is called with different input parameters.

### Bug
The bug lies in how the `run_hive_cmd` function is called with different command strings based on the presence of a partition. In the else block of the function, the command string is not formatted correctly when a partition is provided.

### Strategy for Fixing the Bug
1. Update the command string in the else block to properly format the `show partitions` command when a partition is provided.
2. Ensure that the `run_hive_cmd` function is called with the correct command string and that the output is appropriately checked for table existence.

### Corrected Version

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        partition_spec_str = ','.join(['{0}={1}'.format(k, v) for k, v in partition.items()])
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2})".format(database, table, partition_spec_str))

        return bool(stdout)
``` 

By properly formatting the command string in the else block and checking the output for truthiness to determine whether the table exists, the corrected function should now handle all the expected cases correctly.