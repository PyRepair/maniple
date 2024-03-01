### Bug Analysis:
The bug in the `table_exists` function is due to the condition checks and comparisons being incorrect. The function is supposed to check if a table exists in the specified database, and also handle partition specifications if provided. However, the condition checking logic is flawed which leads to incorrect results.

In the failing test cases:
- Case 1 and Case 3 expect the table to be found in the output, but the current implementation doesn't handle the check properly.
- Case 2 and Case 4 have cases with different capitalizations of the table name, which should still match in the check but currently do not due to the incorrect logic.
- Case 5 and Case 6 test the function with a partition provided, which should also be handled correctly.

### Bug Fix Strategy:
To fix the bug in the `table_exists` function, we need to correct the condition checks to properly handle the existence of tables in the specified database, irrespective of the case of the table name, and also handle partitions if specified.

### Corrected Function:
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

### Correction Rationale:
- Added lowercasing to both the table name being checked and the output from the `run_hive_cmd` to ensure case-insensitive comparison for table existence checks.
- Removed unnecessary conditional return statements to simplify the function and directly return the boolean result of the `stdout` variable.