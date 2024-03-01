### Explain the cause of the bug:
The buggy function `table_exists` in the `HiveCommandClient` class of the `luigi.contrib.hive` module is designed to determine if a given table exists in a Hive database. The bug is related to case sensitivity when checking table names.

The issue arises due to the fact that the function is comparing the table name directly with the table names obtained from the Hive query result. Since Hive is case insensitive, the table names returned might have a different case than the one provided in the function call, leading to false negatives or positives.

### Suggested Strategy for Fixing the Bug:
To fix the bug and make the `table_exists` function case-insensitive, we need to compare the table names in lowercase form. This way, we can match the table names regardless of their case in the Hive query result.

### Corrected Version of the Function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

In the corrected version:
- We convert both the `table` and the table names from the Hive query result to lowercase before comparison, ensuring a case-insensitive check.
- We split the stdout and convert each table name to lowercase using `map(str.lower, stdout.split())` for accurate comparison.

By making these modifications, the `table_exists` function will now correctly handle case sensitivity issues when checking for table existence in Hive.