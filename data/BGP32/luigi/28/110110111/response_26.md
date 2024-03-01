To fix the bug in the `table_exists` function, we need to make the comparison between the table name and the output from the `run_hive_cmd` case-insensitive. This can be achieved by converting both strings to lowercase before comparison.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By converting both `table` and `stdout` to lowercase before comparison, we ensure that the comparison is case-insensitive.

This corrected version should pass all the test cases and satisfy the expected input/output values provided. Additionally, it addresses the issue reported on GitHub by making the `table_exists` function case insensitive.