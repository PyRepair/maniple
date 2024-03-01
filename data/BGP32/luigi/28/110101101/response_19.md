### Bug Analysis:
The bug in the `table_exists` function lies in the conditional checks for the presence of the table in the `stdout` variable. In the first case, the function checks if the `table` is in the `stdout`, which is incorrect as it only denotes if the `stdout` exists, not if it contains the `table`. In the second case, the function checks the existence of the `stdout`, which is also incorrect as it doesn't validate if the table is present. 

### Bug Fix Strategy:
To fix the bug, the function should correctly check if the `table` is present in the `stdout`. This can be achieved by splitting the `stdout` into lines and checking if the `table` is in one of those lines.

### Updated Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout.splitlines()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
        return table in stdout.splitlines()
``` 

By splitting the `stdout` into lines and checking if the `table` is in one of the lines, we ensure that the function correctly verifies the existence of the table. This fix addresses the bug identified in the provided function.