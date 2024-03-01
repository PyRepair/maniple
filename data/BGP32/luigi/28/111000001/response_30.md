## Correction:

The bug in the `table_exists` function lies in the incorrect formatting of the Hive query string when the `partition` parameter is not None. The issue is with the formatting of the query string in the `else` block, specifically in the `%s` placeholder for the partition spec.

To fix the bug, we need to properly format the Hive query string with the partition values. The corrected version of the `table_exists` function is as follows:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        partition_spec = self.partition_spec(partition)
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, partition_spec))

        return bool(stdout)
```

In the corrected version, we store the partition spec value from `self.partition_spec(partition)` in a variable `partition_spec` before using it in the `run_hive_cmd` function. We also replaced the formatting placeholders with proper '{0}', '{1}' syntax in the query string for better readability and correct variable substitution.

This correction addresses the bug and ensures that the Hive query string is properly formatted with the partition spec when checking for table existence.