### Issue Analysis:
The bug in the `table_exists` function is related to case sensitivity when checking if a table exists in Hive. The function is currently not handling case sensitivity correctly, leading to test failures when tables are defined with different case styles.

### Bug Cause:
The bug is due to the function not considering case sensitivity when comparing the table name with the output from the Hive command. Since Hive is case insensitive, the function should convert both the table name and the output to lowercase for comparison.

### Bug Fix Strategy:
To fix the bug, modify the `table_exists` function to convert the table name and stdout to lowercase before comparison to handle case sensitivity properly.

### Corrected Version of the Function:
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

By converting both the table name and the stdout to lowercase, the function now correctly handles case sensitivity and should pass the failing tests.