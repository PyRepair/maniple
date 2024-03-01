### Bug Explanation
The root cause of the bug is that the `table_exists` function is case sensitive when checking if a table exists in Hive. The function compares the table name directly with the result from the Hive command, which might have different case sensitivity. As a result, the function fails to correctly identify table existence in certain cases and leads to failing tests.

### Bug Fix Strategy
To fix the bug, the comparison between the table name and the result from the Hive command needs to be case insensitive. By converting both to lowercase before comparison, the function can properly handle different cases of table names.

### Corrected Function
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

This corrected version of the `table_exists` function now performs a case-insensitive comparison by converting the table name and the Hive command result to lowercase before checking for table existence. This fix should resolve the failing tests related to case sensitivity in table names.