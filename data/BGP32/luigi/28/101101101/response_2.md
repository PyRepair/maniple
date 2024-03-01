### Bug Explanation:
The bug in the `table_exists` function lies in how it checks for the presence of the table in the `stdout`. When `run_hive_cmd` is called to check for the existence of a table, it returns the table name if it exists in the output, but the function incorrectly checks for the presence of the entire output as a string, which leads to incorrect results.

### Bug Fix Strategy:
To fix the bug, we need to modify the condition where we check if the table name is present in the `stdout` instead of checking if the entire `stdout` is present.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        partition_cmd = self.partition_spec(partition)
        stdout = run_hive_cmd("use %s; show partitions %s partition (%s)" % (database, table, partition_cmd))
        return bool(stdout)
``` 

By modifying the condition `table in stdout` in the first if block, we ensure that the function correctly checks if the table name is present in the `stdout` output. Additionally, we return `bool(stdout)` in the second if block to check if the `stdout` is not empty. 

This corrected version of the function should now pass all the failing tests and return the expected results.