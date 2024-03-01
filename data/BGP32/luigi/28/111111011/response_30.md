### Bug Description:
The bug in the `table_exists` function is that it fails to check for the existence of a table case-insensitively. This causes the test cases to fail when checking for tables with different case variations, such as "mytable" and "MyTable". The function only checks if the exact table name is present in the stdout without considering the case.

### Bug Location:
The bug is in the comparison logic when checking if the table name exists in the output (stdout) from the Hive command.

### Bug Cause:
The `table_exists` function compares the table name directly with the stdout without standardizing the case of both. This leads to discrepancies when the table names have different cases.

### Fix Strategy:
1. Standardize the case of the table name and the strings in the stdout for comparison.
2. Update the comparison logic to check for the standardized table name in the standardized stdout.
3. Ensure the comparison is case-insensitive.

### Corrected Version of the `table_exists` Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        partition_str = self.partition_spec(partition)
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, partition_str))
        return bool(stdout)
```

### Changes Made:
1. Standardized the cases of both the `table` and the strings in the `stdout` by converting them to lowercase for case-insensitive comparison.
2. Implemented a case-insensitive comparison for checking the presence of the table name in the `stdout`.
3. Used `bool(stdout)` to directly return the presence/absence of the stdout without additional comparisons. 

By making these changes, the `table_exists` function will now correctly handle case variations in table names and output, resolving the failing test cases.