Based on the error message and the GitHub issues provided, the bug in the `table_exists` function is due to case sensitivity. The function is not checking for table existence in a case-insensitive manner, causing the test to fail.

### Issue:
The `table_exists` function does not handle case sensitivity when comparing the table name extracted from `stdout` with the provided table name.

### Cause of the Bug:
- The function is not converting both the provided table name and the table names in `stdout` to lowercase for a case-insensitive comparison.
- The test cases are failing because they are providing table names in different cases than what is returned by Hive.

### Suggested Fix:
1. Convert both the provided `table` name and the `table` names extracted from `stdout` to lowercase for a case-insensitive comparison.
2. Modify the return statement to use the case-insensitive comparison.

### Corrected Version of the `table_exists` function:
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

By converting both the provided table name and the table names in `stdout` to lowercase, the function will now perform a case-insensitive comparison, addressing the issue reported on GitHub and passing the failing test cases.