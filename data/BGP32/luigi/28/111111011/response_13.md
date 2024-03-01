The bug in the `table_exists` function is related to case sensitivity when checking existing tables in Hive. The function compares the table name with the tables found in the Hive output, but it does not consider case differences, leading to test failures.

### Bug Explanation:
- The function compares the `table` name without considering its case against the tables listed in the `stdout` from Hive.
- If the table name casing does not match exactly, the function incorrectly determines the table existence, leading to assertion errors in the tests.
- The failing test cases demonstrate the discrepancy between the expected (case insensitive) check and the actual behavior of the function.

### Bug Fix Strategy:
To address this issue, the function should convert both the `table` name and the tables in the `stdout` to lowercase for a case-insensitive comparison.

### Corrected `table_exists` Function:
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

By converting both the table name and tables in the Hive output to lowercase for comparison, the function ensures a case-insensitive check. This correction aligns with the suggested fix in GitHub issue #896.

After applying this correction, the `table_exists` function should pass the failing tests and resolve the case sensitivity issue reported on GitHub.