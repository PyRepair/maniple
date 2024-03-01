### Analysis
The buggy function `table_exists` is checking if a table exists in a given database in Hive. The bug seems to be related to how the table name is checked in the output of the `run_hive_cmd` function. In Case 2 and Case 4, the table name in the output is not being correctly matched due to case sensitivity, causing the function to return False when it should return True.

### Bug Explanation
The bug occurs because the `table in stdout` comparison is case-sensitive, and the table names in stdout may not exactly match the table name passed to the function.

### Bug Fix
To fix the bug, we can convert both the table name and the names in the stdout to lowercase before comparison.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```