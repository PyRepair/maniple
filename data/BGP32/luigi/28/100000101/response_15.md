The bug in the provided function lies in the inconsistency in how the output (`stdout`) is being checked for truthiness. In the first branch of the `if` statement, the function checks if `stdout` exists and if the `table` is in `stdout`. This logic is correct. However, in the second branch of the `if` statement, the function only checks if `stdout` exists but doesn't validate its content for the presence of the expected data.

To fix the bug, we need to handle the second branch of the `if` statement in a similar way as the first branch, by checking if the expected data is present in `stdout`.

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout and table in stdout
```

This corrected version ensures that the function checks if the expected `table` is in the output `stdout` for both branches of the `if` statement.

This corrected version should now satisfy all the expected cases provided.