## Analysis:
1. The `table_exists` function in the `HiveCommandClient` class is meant to check if a table exists in a given database with optional partition.
2. The function has two branches, one for when `partition` is None and one for when `partition` is provided.
3. The bug occurs in the case when `partition` is not None, as the `run_hive_cmd` is not correctly constructed.
4. The bug causes the function to always return True when checking for table existence with a partition.
5. To fix the bug, we need to correct the construction of the `run_hive_cmd` in the else branch to properly check for table existence with a partition.

## Bug Fix:
Here is the corrected version of the `table_exists` function:

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, self.partition_spec(partition)))
            
            return stdout is not None
```

By updating the construction of the `run_hive_cmd` in the else branch to include the partition spec in the correct format, the bug is fixed. Now the function will correctly check for the existence of tables with partitions.