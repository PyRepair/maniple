To fix the buggy function `table_exists` and make it case insensitive when checking for table existence, we need to ensure that the table name is converted to lowercase for comparison with the stdout output. This will prevent failures due to case mismatch between the table name and the returned table names from Hive commands.

Here is the corrected version of the `table_exists` function:

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

By converting both `table` and `stdout` to lowercase before the comparison, we ensure that the function is case insensitive while checking for table existence.

This fix addresses the GitHub issue #896 and aligns with the expected behavior described in the failing test cases. The corrected function should now pass the failing tests and provide the expected output values.