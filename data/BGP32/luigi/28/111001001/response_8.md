### Bug Explanation
The bug in the `table_exists` function arises from the condition used to check if a table exists in the specified database. In the first case, the condition `stdout and table in stdout` checks if the `table` string is contained in the `stdout` output. However, the bug occurs due to the case sensitivity of the comparison. Since the table names are case sensitive, this comparison will fail for tables with different cases.

### Bug Fix Strategy
To fix this bug, we need to modify the comparison to be case-insensitive. We can achieve this by converting both the `table` name and the lines in the `stdout` output to lowercase before comparison.

### Corrected Version of the Function
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

By converting both the `table` and the lines in `stdout` to lowercase before comparison, the function will be able to correctly determine if a table exists in the specified database regardless of case sensitivity.