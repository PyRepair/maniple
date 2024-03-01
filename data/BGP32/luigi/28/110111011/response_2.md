### Bug Explanation:

The bug occurs in the `table_exists` method of the `HiveCommandClient` class in the `luigi.contrib.hive.py` file. The issue stems from the comparison of the table name retrieved from Hive with the input table name provided to the method. In some cases, the table names are compared in a case-sensitive manner, leading to test failures when the table names do not match due to case differences.

The failing tests illustrate scenarios where the test for table existence fails due to case sensitivity in the comparison. The issue has been identified on GitHub with a proposed fix to make the comparison case insensitive.

### Bug Fix Strategy:
To fix this bug, we need to modify the `table_exists` method to compare table names in a case-insensitive manner. By converting both the input table name and the table names retrieved from Hive to lowercase before comparison, we can ensure that the comparison is not affected by case differences.

### Corrected Function:
Here is the corrected version of the `table_exists` method:

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

This corrected version ensures that the comparison of table names is case insensitive, addressing the bug and making the `table_exists` method more robust.