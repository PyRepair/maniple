### Bug Explanation
The bug in the `table_exists` function lies in the condition checking for the existence of the table. When checking if the `table` exists in the `stdout`, the function is not handling case sensitivity properly. It simply checks if the `table` is in the `stdout`, which may not work correctly when the case of the table name differs.

### Bug Fix Strategy
To fix the bug, we need to make the table check case-insensitive. We can achieve this by converting both the `table` and `stdout` to lowercase before performing the check.

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

By making both the `table` and `stdout` lowercase before performing the check, the function will now accurately handle cases where the table name's casing differs in the `stdout`. This corrected version should now pass the failing test cases.