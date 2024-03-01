### Bug Explanation:
The bug in the `table_exists` function lies in the comparison of the `table` value with the `stdout` value returned from the `run_hive_cmd` function. The issue arises due to case sensitivity, where the `table` value is not being compared in a case-insensitive manner with the `stdout` value, leading to test failures.

### Bug Fix Strategy:
To fix the bug, we need to modify the comparison operation to be case-insensitive. This can be achieved by converting both the `table` value and the `stdout` value to lowercase before comparison.

### Corrected Version of the Function:
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

By converting both `table` and `stdout` to lowercase before comparison, the function will now perform a case-insensitive check, as required by the GitHub issue. This corrected version should pass the failing test cases and fix the bug related to case sensitivity in table existence checks.