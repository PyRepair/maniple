### Bug Explanation:

The buggy function `table_exists` is not correctly checking for the existence of a table in a Hive database when a partition is specified. The issue lies in the way the `run_hive_cmd` function is being called with the `stdout` variable to determine if the table exists. The current implementation checks if `stdout` is not empty, which might not be the correct logic depending on the output of the `run_hive_cmd` function.

### Bug Fix Strategy:

To fix this bug, we need to modify the logic in the `table_exists` function to properly handle the case where a partition is specified. We should check the output of the `run_hive_cmd` function for the existence of the table based on the specified conditions.

### Corrected Code:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.strip().split()
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition)))
        return table in stdout.strip().split()
```

By splitting the `stdout` output and checking if the table name is in the resulting list, we ensure a more accurate check for the table's existence even when partitions are involved.