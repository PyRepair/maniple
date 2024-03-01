### Explanation of Bug:

The bug in the `table_exists` function lies in the comparison between the table name and the output of the `run_hive_cmd` function. The comparison is case-sensitive, causing the function to fail when the table names do not match case exactly.

The failing test cases highlight this issue as they expect case-insensitive table existence checks. The test cases are failing due to the inaccurate comparison between the table name and the output.

To address this bug, it is necessary to modify the function to perform a case-insensitive comparison when checking if a table exists.

### Bug Fix Strategy:
1. Modify the comparison statement to use case-insensitive matching between the table name and the output from `run_hive_cmd`.
2. Convert both the table name and the output to lowercase before comparison.

### Corrected Version of the Function:

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

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

By making this modification, the `table_exists` function should now pass the failing test cases and be case-insensitive when checking for table existence.