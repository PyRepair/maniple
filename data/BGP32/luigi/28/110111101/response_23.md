### Bug Explanation
The bug in the `table_exists` function lies in the conditional statement checks for the existence of the table and handling partitions. The bug causes the function to return incorrect values based on the `stdout` variable. In Case 1 and Case 3, the function does not handle the presence of the table correctly, resulting in the test failures.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function correctly checks for the presence of the table in the Hive database. When dealing with partitions, it should also account for the partition information provided.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By making the above changes, we ensure that the function properly handles the table existence and partition checks, resolving the bug and passing the failing tests.