### Bug Explanation
The bug is in the `table_exists` function of the `HiveCommandClient` class. The issue arises because the function checks if a table exists in a database but does not handle the case sensitivity properly when checking for table names. This results in the test cases failing when checking table existence with different case variations.

### Bug Fix Strategy
To fix the bug, we need to ensure that the table name comparison is case insensitive. We can achieve this by converting both the table name from input and the table names obtained from the output to lowercase before comparing them.

### Corrected Function

```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

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

By converting both the table name from input and the table names obtained from the output to lowercase before comparison, we ensure that the function is case insensitive when checking for the existence of tables. This corrected version of the function should pass the failing test cases and handle case sensitivity for table names properly.