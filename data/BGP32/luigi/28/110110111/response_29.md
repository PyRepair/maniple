The buggy function `table_exists` in the `HiveCommandClient` class of the `luigi.contrib.hive` file needs to be fixed. The issue arises from case sensitivity when comparing the table name with the output from Hive commands. The function should perform a case-insensitive comparison to handle table names correctly.

### Analysis:
- **Buggy Function `table_exists`:**
  - The function checks if a table exists in a database using Hive commands.
  - It encounters issues with case sensitivity due to mismatched table names.
  
- **Failing Test `test_table_exists` in `hive_test.py`**:
  - Fails due to incorrect handling of case sensitivity in table names.
  - The assertion error is raised because the function is not returning the expected values in a case-insensitive manner.
  
- **Expected Input/Output Values**:
  - The function should correctly match table names with the case-insensitive output from Hive commands to return the correct boolean value.
  
- **GitHub Issue #896**:
  - Indicates the need to make the `table_exists` function case insensitive to handle table names accurately.

### Bug Fix Strategy:
To fix the bug, we need to modify the `table_exists` function to perform case-insensitive comparisons when checking table existence. We should compare the lowercase version of the table name with the lowercase output from Hive commands to handle case discrepancies.

### Corrected Function `table_exists`:
```python
# The corrected `table_exists` function
def table_exists(self, table, database='default', partition=None):
    table_lower = table.lower()
    
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table_lower))
        return stdout and table_lower in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table_lower, self.partition_spec(partition)))
        
        return bool(stdout)
```

This corrected version of the `table_exists` function ensures that case sensitivity issues are handled by converting both the table name and the output to lowercase for comparison.

By implementing this change, the `table_exists` function should now pass the failing test cases and successfully address the GitHub issue related to case insensitivity in table existence checks.