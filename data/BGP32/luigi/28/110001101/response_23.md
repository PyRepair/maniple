### Bug Explanation
The bug in the `table_exists` function lies in the logic used to check if a table exists in the specified database. In the first case, when `partition` is `None`, the function only checks if the `table` is in the `stdout` returned from the hive command, which may lead to false positives. In the second case, with a non-None `partition`, the function constructs the command incorrectly which can also lead to issues in detecting table existence.

### Bug Fix Strategy
To fix the bug, we need to modify the logic of the function to ensure that it accurately checks for table existence regardless of the presence of a partition. We should modify how the command is constructed and how the output is checked.

### Corrected Function
```python
# The relative path of the corrected file: luigi/contrib/hive.py

# The corrected version of the buggy function
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables in {1};'.format(database, table))
    
            return table in stdout.split('\n')
        else:
            stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition)))
    
            return bool(stdout)
```

By separating the logic for table existence check based on the presence of a partition and adjusting how the command is constructed, the corrected function ensures accurate detection of table existence.