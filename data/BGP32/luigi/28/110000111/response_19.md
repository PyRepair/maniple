### Analysis
The `table_exists` function in the `HiveCommandClient` class is supposed to check if a table exists in a specific database with an optional partition. The issue reported on GitHub mentions that the function should be case insensitive when checking table names due to inconsistencies in capitalization.

### Identified Errors
1. The function only compares the exact table name with the tables in the database, leading to case sensitivity issues.
2. The function does not handle the case where the returned tables' names might be in lowercase while the input table name is in a different case.

### Bug Cause
The bug occurs because the function does not account for case sensitivity differences between the input table name and the names of the tables returned by Hive. This leads to inconsistencies when comparing table names.

### Fix Strategy
To fix the bug, we should ensure that the comparison between the input table name and the tables returned by Hive is case insensitive. We can achieve this by converting both names to lowercase before comparison.

### Corrected Function
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

            return stdout and table.lower() in map(str.lower, stdout.splitlines())
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

            return bool(stdout)
```

This corrected version of the function ensures that the comparison between the input table name and the tables returned by Hive is done in a case-insensitive manner. The input table name and the names of the returned tables are converted to lowercase before comparison, resolving the case sensitivity issue reported on GitHub.