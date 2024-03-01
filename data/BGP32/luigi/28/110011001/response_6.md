### Bug Explanation
The bug in the `table_exists` function lies in how the function checks for the existence of the table. In the first branch of the if-else statement, the function executes a Hive command to check if a table exists by showing tables like the provided table name. However, in the second branch, the function is attempting to show partitions without checking the existence of the table first, leading to unexpected behavior.

### Bug Fix
To fix the bug, we need to ensure consistency in how we check for the existence of the table. We should first check if the table exists before attempting to show partitions.

### Corrected Version of the Function
```python
class HiveCommandClient(HiveClient):

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table in stdout
        else:
            table_check = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table)
            if table_check and table in table_check:
                stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
                return bool(stdout)
            else:
                return False
``` 

By modifying the function as above, we now first check for the existence of the table before attempting to show partitions. This revision maintains consistency in how the function verifies table existence and should address the bug.