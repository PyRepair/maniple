### Bug Explanation
The bug in the `table_exists` function is due to the comparison logic when checking if the table exists in the output of the `run_hive_cmd` function. The buggy function is expecting the table name to be present in the exact same format as it was provided, which causes the bug when checking for table existence with case-sensitive table names.

### Bug Fix Strategy
To fix this bug, we need to update the comparison logic to perform a case-insensitive check when verifying if the table name exists in the `stdout` variable returned from `run_hive_cmd`.

### Corrected Version of the Function
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and any(t.lower() == table.lower() for t in stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By using the `any` function to check if any table in `stdout` matches the provided `table` name in a case-insensitive manner, and returning `True` if any match is found, we can ensure the function works correctly for both case-sensitive and case-insensitive table name comparisons.