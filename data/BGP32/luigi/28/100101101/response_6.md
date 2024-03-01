### Bug Fix Strategy:
The bug seems to be related to how the output of the `run_hive_cmd` function is processed in the `table_exists` function. The function is currently checking if the table name is in the output string, which can lead to incorrect results, especially when the table name is a substring of another table name.

To fix this bug, we should modify the logic to correctly handle the output of the `run_hive_cmd` function by splitting the output into lines and comparing each line with the table name.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.splitlines()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

This corrected version of the `table_exists` function splits the stdout into lines using the `splitlines()` method before checking if the table name is in the output. This should handle the issue of incorrect matching on substring table names.