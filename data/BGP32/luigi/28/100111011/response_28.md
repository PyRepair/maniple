### Analysis:
1. The `table_exists` function is failing the test due to case sensitivity. It should be case insensitive when checking for the existence of a table.
2. The function compares the table name directly with the output without considering case variations.
3. The failing test cases show that the function fails when the case of the table name doesn't match exactly with the output.
4. To fix the bug, we need to convert both the table name and the output to lower case for comparison.

### Bug Fix:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()  # Convert to lower case for case-insensitive check
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By converting both the table name and the output to lower case, the function will now perform a case-insensitive check for table existence.

This fix addresses the issue raised in the GitHub topic "Fix #896: make table_exists case insensitive".