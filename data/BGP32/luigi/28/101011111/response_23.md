To fix the bug in the `table_exists` function, we need to make the comparison case-insensitive by converting both the table name and the stdout to lowercase before checking. This will ensure that the function behaves correctly regardless of the case of the table name.

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

By converting both the table name and the stdout to lowercase before comparison, we ensure that the function is case-insensitive when checking for table existence.

This corrected version should pass the failing tests and satisfy the expected input/output values. It addresses the GitHub issue related to making the `table_exists` function case-insensitive.