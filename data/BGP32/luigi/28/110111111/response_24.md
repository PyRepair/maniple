To fix the bug in the `table_exists` function, we need to modify the comparison between the table name and the output of the Hive command in a case-insensitive manner. This will ensure that the function can correctly determine if a table exists regardless of the case.

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

By converting both the table name and the stdout to lowercase before comparison, we ensure that the function is case-insensitive when checking for table existence. This correction aligns with the GitHub issue raised regarding making the `table_exists` function case-insensitive.

With this correction, the `table_exists` function should now pass the failing test cases and meet the expected input/output values provided.