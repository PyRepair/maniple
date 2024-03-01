### Bug Explanation:
The bug in the `table_exists` function lies in the conditional checks for the existence of the table. In the first case, the function incorrectly returns `table in stdout` without considering the specific format of the output from the `run_hive_cmd` function. This causes the function to return False even when the table exists.

The second case fails because the function does not account for case insensitivity when checking table names. Since the `table` variable is not normalized, it leads to incorrect comparisons and, consequently, incorrect results.

### Bug Fix Strategy:
1. Update the function to handle the output of `run_hive_cmd` properly. It should check if the table name is present in the stdout without relying on the exact match.
2. Normalize the table name before comparison to ensure case insensitivity does not affect the result.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and any(table.lower() == t.lower() for t in stdout.splitlines())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By normalizing the table names for comparison and adjusting how the stdout is checked, the corrected function should now pass the failing tests and provide the expected results for the input cases.