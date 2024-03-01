### Analysis:
1. The `table_exists` function is failing the test cases due to case sensitivity in comparing the table names.
2. The function is comparing the table names directly without considering case sensitivity, leading to false results.
3. The bug occurs because the function does not check for case insensitivity when comparing the table names with the output from the `run_hive_cmd` function.
4. To fix the bug, we need to convert both the table name and the output to lowercase (or uppercase) before comparing them.

### Bug Fix:
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

This revised function ensures that both the table name and the output are converted to lowercase before comparison, making the check case insensitive.

By making this simple adjustment, the `table_exists` function should now pass the failing test cases and satisfy the expected input/output values while addressing the GitHub issue related to case insensitivity in table existence checks.