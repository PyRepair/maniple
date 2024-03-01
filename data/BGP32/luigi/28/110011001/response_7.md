### Bug Explanation
The bug in the `table_exists` function is due to the comparison of the `table` name in the `stdout`. In the if branch of the function, the comparison is done using `table in stdout`, which checks if the exact table name is present in the `stdout`. However, in the else branch, the function checks if the `stdout` is not empty (`True` if `stdout` is not empty) without validating the table name. This leads to incorrect results in the function return.

### Bug Fix Strategy
To fix the bug, we need to ensure that the table name comparison is consistent in both branches of the function. We should check if the table name is present in the `stdout` for both cases to determine if the table exists.

### Corrected Version of the Function
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
            return stdout and table in stdout
```

By modifying the else branch to also include the table name comparison (`table in stdout`), the function will consistently check if the table exists based on the `stdout` output.