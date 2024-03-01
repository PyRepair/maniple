To fix the bug in the `table_exists` function, we need to make the comparison case insensitive by converting both the table name and the stdout to lowercase before the comparison. This will address the issue raised in the GitHub report and allow the function to correctly handle case discrepancies.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1}
                ({2})""".format(database, table, self.partition_spec(partition)))
        return bool(stdout)
```

By converting both the table name and the `stdout` to lowercase before comparison, we ensure that case discrepancies do not affect the function's behavior.

This corrected version of the function should pass the failing test cases and satisfy the expected input/output values and the GitHub issue's requirements.