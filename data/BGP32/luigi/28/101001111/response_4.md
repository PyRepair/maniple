## Bug Explanation:
The buggy function `table_exists` in the `HiveCommandClient` class of the `luigi/contrib/hive.py` file is failing to accurately determine if a table exists in Hive due to a case sensitivity issue. When checking for the existence of a table, it compares the table name directly with the output from the Hive command, which is case-sensitive. As Hive is case-insensitive regarding table names, this comparison leads to incorrect results.

## Bug Fix Strategy:
To fix this bug, we need to ensure that the comparison between the table name and the output from the Hive command is case-insensitive. By converting both strings to lowercase before comparison, we can accurately determine if the table exists irrespective of the case.

## Corrected Version:

```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

            return bool(stdout)
```

In the corrected version:
- We convert both the `table` and `stdout` strings to lowercase using `.lower()` before performing the comparison.
- By making this change, the function will be able to correctly identify if the table exists in Hive regardless of the case sensitivity.

This fix addresses the issue reported on GitHub and ensures that the `table_exists` function behaves as expected in a case-insensitive manner when checking for table existence in Hive.