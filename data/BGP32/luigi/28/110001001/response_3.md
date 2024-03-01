### Bug Explanation
The bug in the `table_exists` function lies in the comparison condition used to check if the table exists in the database. In the current implementation, the function checks if the table name is in the stdout output obtained from running the Hive command. However, the comparison is case-sensitive, which leads to incorrect results when the case of the table name does not match exactly with the one returned from the Hive command.

### Bug Fix Strategy
To fix the bug, we need to modify the comparison to be case-insensitive when checking if the table exists in the database.

### Corrected Version of the function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

In the corrected version, we convert both the queried table name and the returned table names from Hive to lowercase before comparing them. This ensures a case-insensitive check for table existence, fixing the bug.