### Analysis:
1. The `table_exists` function in the `HiveCommandClient` class is supposed to check if a table exists in a given database.
2. The bug seems to be related to case sensitivity of table names causing the test cases to fail.
3. The issue on GitHub suggests making the `table_exists` function case insensitive to address this problem.
4. To fix the bug, we need to modify the function to compare the table name in a case-insensitive manner.
5. We will update the function to convert both the table name and output from `stdout` to lowercase for comparison.

### Bug Fix:
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
            return bool(stdout)
```

By converting both the table name (`table`) and the output (`stdout`) to lowercase before comparison, we ensure a case-insensitive check for table existence. This should resolve the failing test cases and address the GitHub issue related to table case sensitivity.