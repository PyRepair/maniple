### Bug Explanation
The bug in the `table_exists` function lies in the conditional check of the `stdout` variable. The function checks if `stdout` exists and if the provided `table` name is in `stdout`, which is causing the incorrect behavior. The function should check if the `stdout` contains the exact match of the table name instead of just checking if it exists.

### Fix Strategy
To fix the bug, we need to modify the conditional check for `stdout` to ensure that the exact table name is present in the `stdout` output. This will accurately determine if the table exists in the database or not.

### Corrected Function
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.splitlines()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

This corrected version splits the `stdout` by lines to accurately check if the exact table name is present in the output.

With this correction, the function should pass the failing tests and match the expected input/output values.