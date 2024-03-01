### Bug Explanation:
The buggy function `table_exists` in the `HiveCommandClient` class of the `luigi.contrib.hive` file has a bug related to case sensitivity in table existence checks. Specifically, the function uses a case-sensitive check to determine if a table exists in the database, leading to test failures when the table name's case is different in the actual database.

The function queries Hive to show tables or show partitions based on the provided parameters and then tries to match the requested table name against the output. The bug arises from directly comparing the table name against the standard output, which may have a different case due to Hive's case insensitivity.

### Bug Fix Strategy:
To fix the bug and make the `table_exists` function case insensitive when checking for table existence, you need to compare the lowercased table name with the lowercased stdout to ensure a consistent case comparison.

### Corrected Version:

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

In the corrected version, the table name and the output from Hive are both converted to lowercase using the `lower()` method before comparison to ensure a case-insensitive check for table existence.

This modification aligns with the reported issue on GitHub and caters to scenarios where the table names may have varying cases but should still be considered as existing tables.