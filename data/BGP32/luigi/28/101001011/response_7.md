### Analysis:
The issue reported on GitHub indicates that the `table_exists` function is not case insensitive, causing failures when checking for tables with different capitalization than expected. The function compares the table name directly to the output from Hive, which may be in lowercase, leading to false negatives.

### Bug in the Buggy Function:
The bug in the `table_exists` function is that it compares the table name without considering case sensitivity directly to the output from Hive. This comparison can lead to incorrect results, especially when the table names have different capitalization.

### Bug Fix Strategy:
To fix the bug, we need to make the comparison case insensitive by converting both the table name and the stdout from Hive to lowercase before checking for existence.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

### Explanation:
The corrected version of the `table_exists` function ensures that both the table name and the output from Hive are converted to lowercase before comparison, making the check case insensitive as requested in the GitHub issue. This modification will prevent issues related to table name capitalization discrepancies when checking for table existence.