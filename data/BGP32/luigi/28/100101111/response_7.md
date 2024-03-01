### Bug Analysis:
1. The `table_exists` function in the `hive.py` file is not case insensitive when checking if a table exists in Hive.
2. The failing test cases highlight the issue when trying to check for tables with different casing than stored in Hive.
3. The buggy function does not handle case insensitivity when matching table names from the Hive output.
4. The correct behavior should be to convert both the table name and the Hive output to lower case for case-insensitive comparison.

### Bug Fix Strategy:
1. Modify the `table_exists` function to convert both the table name and the Hive output to lower case before comparison.
2. This modification will ensure case insensitivity when checking for table existence in Hive.
3. Update the `table_exists` function to handle case sensitivity correctly by converting all strings to lower case.

### Corrected Function:
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

By making this change, the `table_exists` function will now handle case insensitivity when checking for table names in Hive, resolving the issue highlighted in the failing tests and the GitHub issue.