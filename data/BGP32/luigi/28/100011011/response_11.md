### Bug Analysis:
1. The `table_exists` function is not handling case insensitivity when comparing the table name from stdout.
2. The failing tests are due to the mismatch in case sensitivity between the input table name and the table name extracted from stdout.
3. The suggested fix in the GitHub issue is to check the table name in lowercase to avoid case issues.

### Bug Fix Strategy:
1. Modify the comparison between the table name and the table name extracted from stdout to be case insensitive by converting both to lowercase.
2. Update the `table_exists` function to implement a case-insensitive comparison for table names.

### Corrected Function:
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

### Updated Function Explanation:
1. Lowercase both the input table name and the extracted table names from stdout for a case-insensitive comparison.
2. This change ensures that the comparison considers table names irrespective of their case.

By making this update, the corrected function should successfully pass the failing tests and resolve the case sensitivity issue mentioned in the GitHub issues.