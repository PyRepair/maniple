### Analysis:
1. The `table_exists` function in the `HiveCommandClient` class appears to be failing the test cases due to case sensitivity in table name comparison.
2. The bug is likely arising because the comparison between the table name and the output from the Hive command is case sensitive, causing the tests to fail.
3. The failing test cases demonstrate that the returned values from the `run_hive_cmd` function are not being compared correctly with the table name due to case discrepancies.
4. To fix the bug, we need to ensure that the comparison between the table name and the output is case insensitive.

### Solution:
To fix the bug, we will modify the `table_exists` function to perform a case-insensitive comparison between the table name and the output from the Hive command.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By using `table.lower()` and `stdout.lower()` in the comparison, we ensure that the table name comparison is performed in a case-insensitive manner.

This modification aligns with the suggested fix in GitHub issue #896 and addresses the failing test cases related to case sensitivity.