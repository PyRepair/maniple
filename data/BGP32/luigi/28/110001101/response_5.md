### Bug Explanation
The bug in the `table_exists` function comes from incorrectly checking if the table exists based on the output of the `run_hive_cmd` function. In the first branch of the `if` statement where `partition` is None, the function checks if the `table` is in the `stdout`, but the comparison is incorrect. The second branch where `partition` is not None constructs a Hive query to show partitions, but the logic to determine if the table exists is flawed.

### Bug Fix Strategy
To fix the bug in the `table_exists` function, we need to correct the comparison when `partition` is None to properly check for table existence in the `stdout`. Additionally, we need to adjust the logic when `partition` is not None to correctly determine if the table exists based on the `self.partition_spec(partition)`.

### Corrected Version of the Function
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table in stdout.strip().split('\n')
        else:
            stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition)))
            return len(stdout.split('\n')) > 1
```

In the corrected version:
1. In the case where `partition` is None, we properly split the `stdout` by newlines and check if the `table` is in the result.
2. In the case where `partition` is not None, we split the `stdout` by newlines and check if there are partitions displayed for the given table, indicating that the table exists.