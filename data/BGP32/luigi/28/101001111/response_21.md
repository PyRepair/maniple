The bug in the `table_exists` function is that it checks the existence of a table in a case-sensitive manner, leading to failures when the table name's case does not match the case returned by Hive. The fix involves converting both the table name and the output of the Hive command to lowercase for comparison.

### Bug Cause:
The bug is caused by the `table_exists` function not handling case sensitivity when comparing the table name with the output from the Hive command. If the table name's case does not match the case of the tables returned by Hive, the function incorrectly reports the table as non-existent.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the `table_exists` function to convert both the table name and the output of the Hive command to lowercase before comparison. This way, the function will perform a case-insensitive check for table existence.

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

By converting both the table name and the output to lowercase before comparison, the function now correctly handles case-insensitive table existence checks as expected. This fix aligns with the reported GitHub issue and resolves the problem identified.