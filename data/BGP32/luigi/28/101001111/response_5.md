### Bug Explanation:

The bug in the `table_exists` function arises from a case sensitivity issue when comparing the table name extracted from the Hive command output (`stdout`) with the input table name. Hive is case-insensitive, so the comparison should be case-insensitive as well to accurately determine table existence.

### Bug Fix Strategy:

To fix the bug, modify the comparison between the extracted table name and the input table name to be case-insensitive. This can be achieved by converting both names to lowercase before comparison.

### Corrected Version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd(
            """use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

This corrected version ensures that the table name comparisons are case-insensitive by converting both the input table name and the extracted table names from the Hive command output to lowercase before checking for existence.