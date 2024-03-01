### Bug Explanation
The bug in the `table_exists` function arises from a case sensitivity issue when comparing the table name extracted from the `stdout` with the provided `table` input. Since Hive is case insensitive, the comparison should also be case insensitive to ensure correct behavior.

### Bug Fix Strategy
To fix the bug, we need to make the comparison case insensitive by converting both the `table` and the extracted table names from `stdout` to lowercase before comparing them.

### Corrected Version
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

In this corrected version, both the `table` and the content of `stdout` are converted to lowercase before comparison, ensuring that the check is case insensitive as required to address the issue reported on GitHub.