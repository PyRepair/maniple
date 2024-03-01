### Bug Explanation
The bug in the `table_exists` function arises from the conditional check in the if/else statement. The function incorrectly returns `stdout and table in stdout` for the case where a partition is not specified, which is not the correct behavior. Also, the second part of the conditional check in the else statement doesn't accurately determine if a table exists.

### Bug Fix Strategy
To fix the bug, we need to modify the conditional checks in the function. When a partition is not specified, the function should check if the table name is in the stdout. When a partition is specified, the function should use the correct command to check for the existence of the table and partition. 

### The Corrected Version
```python
# The relative path of the corrected file: luigi/contrib/hive.py

from luigi.contrib.hive import HiveClient, run_hive_cmd

class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout.strip() == table  # Check if the table name matches exactly in the stdout
        else:
            stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2})'.format(database, table, self.partition_spec(partition)))
            return stdout.strip() != ""  # Check if the stdout is not empty to confirm table and partition existence
```

By making the corrections as suggested, the `table_exists` function now correctly checks for the existence of tables and partitions in the Hive database. This corrected version should pass the failing tests provided.