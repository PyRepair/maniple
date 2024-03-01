### Bug Explanation:
The current implementation of the `table_exists` function is case-sensitive when checking if a table exists in Hive. The issue arises when comparing the provided table name with the table names returned by the Hive command. The bug causes tests to fail when looking for tables with different case variations.

### Bug Location:
The bug is located in the condition where the function checks if the provided table exists in the Hive output. The comparison `table in stdout` directly compares the table name without considering case sensitivity.

### Cause of the Bug:
The bug causes failed tests when expecting tables with different letter cases than the ones returned by Hive due to the case-sensitive comparison. The function does not handle case variations elegantly, leading to inconsistent test results.

### Suggested Fix:
To fix the bug and make the table existence check case-insensitive, convert both the provided table name and the table names in the Hive output to lowercase before comparison. This adjustment will ensure that the function accurately detects the existence of tables regardless of case variations.

### Corrected Code:
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

By modifying the table comparison to `table.lower() in stdout.lower()`, the function now performs a case-insensitive check for table existence, addressing the bug and ensuring consistency with the expected behavior.