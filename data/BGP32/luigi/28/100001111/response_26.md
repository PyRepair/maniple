The buggy function `table_exists` is not handling case sensitivity when checking for table existence in Hive, leading to failing tests due to case mismatches between the input table name and the retrieved table names from Hive.

### Bug Identification:
The buggy function is comparing the table names directly without considering the case sensitivity. This causes issues when the table name case doesn't match as Hive is case-insensitive and returns table names in lowercase.

### Bug Cause:
The bug arises from the comparison between the input table name and the retrieved table names from Hive without considering the case sensitivity. This leads to false negatives where table names are considered non-existent due to case mismatches.

### Bug Fix Strategy:
To fix the bug, we need to ensure a case-insensitive comparison between the input table name and the retrieved table names from Hive. We can achieve this by converting both the input table name and the retrieved table names to lowercase for comparison.

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

By converting both the input table name and the retrieved table names to lowercase before comparison, the corrected function ensures a case-insensitive check for table existence in Hive, addressing the bug reported in the GitHub issue.