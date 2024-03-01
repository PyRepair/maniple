### Bug Explanation
The bug in the `table_exists` function arises from the way it checks for the existence of a table in the specified database. The function uses the output of `run_hive_cmd` to determine if the table exists or not. In the case where `partition` is `None`, the function checks if the table name is in the output of `run_hive_cmd` after executing a command to show tables like the specified table name. However, the bug occurs because the function doesn't account for case sensitivity in table names, leading to incorrect results.

### Bug Fix Strategy
To fix this bug, we need to ensure that the comparison between the table name and the output of `run_hive_cmd` is case-insensitive. This can be achieved by converting both the table name and the output to lowercase before comparison.

### Corrected Version
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
```

In this corrected version, both the table name and the output of `run_hive_cmd` are converted to lowercase using the `lower()` method before the comparison. This ensures that the comparison is case-insensitive and fixes the bug in the function.