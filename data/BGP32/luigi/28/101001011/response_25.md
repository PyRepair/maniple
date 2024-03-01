### Bug Explanation:
The bug in the `table_exists` function arises from a case sensitivity issue. The function is checking for the existence of a table in Hive by comparing the table name provided as input with the table names retrieved from Hive, which might be in a different case due to Hive being case-insensitive. This leads to false negatives when trying to identify the existence of tables with different casing.

### Bug Fix Strategy:
To fix this bug, we should convert both the table name provided and the table names retrieved from Hive to lowercase before comparison. This ensures a case-insensitive match and prevents false negatives.

### Corrected Version of the Function:
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

By converting both `table` and the table names retrieved from Hive to lowercase before comparison, the corrected function ensures that the check for table existence is case-insensitive, fixing the bug reported in the GitHub issue.