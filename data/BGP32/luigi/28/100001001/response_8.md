### Bug Explanation:
The buggy function `table_exists` is checking if a given table exists in a database by running a Hive command. The bug occurs due to the comparison of the table name in the returned stdout. The comparison is case-sensitive, causing inconsistencies based on the case of the table name.

### Bug Location:
The bug is in the comparison `table in stdout`. This comparison will return `False` if the case of the table name in the database does not match exactly with the case of the table name in the `stdout`.

### Bug Fix:
To fix the bug, we can convert both the table names to a consistent case, for example, lowercase or uppercase, before comparing them. This way, the comparison will be case-insensitive.

### Corrected Version:
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

In the corrected version, both the `table` name and `stdout` are converted to lowercase using the `lower()` method before comparison. This ensures a case-insensitive comparison for checking if the table exists in the database.