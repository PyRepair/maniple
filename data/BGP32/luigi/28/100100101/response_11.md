### Bug Explanation
The buggy function `table_exists` has an issue where it always returns `True` or `False` based on the presence of `stdout`, which is not correctly handling the logic for checking if the table exists in the Hive database. The function should check if the table name is present in the output, not just if there is any output.

### Bug Fix Strategy
To fix the bug, we need to modify the logic to correctly check if the table name is present in the output when partition is None and handle the partition case correctly as well.

### Corrected Version of the Function
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        tables = stdout.split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        partitions = stdout.split('\n')
        return bool(partitions)
```

By splitting the `stdout` response and searching for the table name or partitions within the split lines, the corrected function will now properly determine if the table exists in the database.