### Analysis
The buggy function `table_exists` in the `HiveCommandClient` class is supposed to check if a table exists in a given database. The bug seems to be related to how the function handles partitions. In the current implementation, the function is not correctly checking for the existence of tables with partitions.

### Bug
The bug is in the `else` block of the `table_exists` function. The function constructs a Hive command using `self.partition_spec(partition)` to get the partition specification for the table. However, it expects the output to be a single string, which is causing issues in comparison.

### Fix
We need to modify the `table_exists` function to properly handle partitions when checking for table existence in the Hive metastore. The condition for the presence of the table in the `else` block should be based on whether the table is present in the `stdout` result of the command.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        partition_spec = self.partition_spec(partition)
        stdout = run_hive_cmd('use %s; show partitions %s' % (database, table))

        return partition_spec in stdout.splitlines()
``` 

After applying this fix, the `table_exists` function should correctly handle checking for the existence of tables with or without partitions in the Hive metastore.