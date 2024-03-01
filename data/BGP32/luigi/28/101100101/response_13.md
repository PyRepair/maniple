### Bug Explanation
The bug in the `table_exists` function occurs due to the logic in the if-else block where the condition is checking for the presence of `stdout` rather than the presence of the table name in `stdout`. This results in incorrect evaluation of whether the table exists or not. Additionally, in the case where a partition is specified, the formatting of the `stdout` value is incorrect, leading to a false negative.

### Fix Strategy
To fix the bug, we need to adjust the logic in the if-else block to properly check for the table name in `stdout`. Additionally, we need to correct the formatting when a partition is specified to match the expected `stdout` output.

### Corrected Code
```python
# The corrected version of the buggy function
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table in stdout
        else:
            partition_str = ', '.join(['{0}={1}'.format(k, v) for k, v in partition.items()])
            stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                                    ({2})""".format(database, table, partition_str))
            return bool(stdout)
```

Now, the corrected `table_exists` function properly checks for the existence of the table name in `stdout` and formats the partition string correctly before checking for its presence in the output. This should resolve the issue and make the function pass the failing test cases.