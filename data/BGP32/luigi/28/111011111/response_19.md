### Identified Bug:
The bug in the `table_exists` function is that when checking if a table exists, it does a case-sensitive comparison between the table name and the output from the Hive command. This leads to failing tests when the table name casing mismatches the output.

### Cause of the Bug:
- The failing tests indicate that when the table name in the function call is in a different case than the actual table name stored in stdout, the comparison fails.
- The code does not accommodate for case-insensitivity in table name checking.
- The bug is causing the tests to fail in scenarios where the table names differ only in case.

### Fix Strategy:
To fix this bug, we need to make the comparison between the table name and the output case-insensitive.
- Adjust the function to convert both the table name and the output to lowercase before performing the comparison.
- This approach ensures that the comparison is independent of the casing of the table name.

### Updated Corrected Function:
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

### Summary:
The corrected version of the `table_exists` function fixes the bug by converting both the table name and the stdout to lowercase before comparing them. This ensures a case-insensitive check for table existence, resolving the failing tests and aligning with the GitHub issue's request for case insensitivity.