The buggy function `table_exists` in the `HiveCommandClient` class of the `luigi/contrib/hive.py` file is not case insensitive when checking for the existence of a table in Hive. This causes discrepancies when comparing the table name in different cases.

The issue arises from the comparison between the table name and the table names returned by Hive, which are in lower case. This leads to false negatives when checking for the existence of a table.

To fix this bug:
1. We need to convert both the table name and the table names returned by Hive to lowercase for a case-insensitive comparison.
2. Update the comparison logic to check if the lowercase table name is in the lowercase stdout from Hive.

Here is the corrected version of the `table_exists` function:

```python
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd('''use {0}; show partitions {1} partition
                            ({2})'''.format(database, table, self.partition_spec(partition)))
            return bool(stdout)
```

In this revised version, both the table name and the output from Hive are converted to lowercase before the comparison. This ensures a case-insensitive check for the existence of the table in Hive.