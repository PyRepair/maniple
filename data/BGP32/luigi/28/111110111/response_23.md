Looking at the buggy function `table_exists`, the issue arises when checking if the table name exists in the output string obtained from `run_hive_cmd`. Currently, the comparison is case-sensitive, leading to test failures when table names have different casing. To fix this issue and make the function case-insensitive, we need to convert both the table name and the output string to lowercase before the comparison.

Here is the corrected version of the `table_exists` function:

```python
# The corrected version of the buggy function
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

In this corrected version, `table.lower()` and `stdout.lower()` are used for a case-insensitive comparison. This modification ensures that the function behaves correctly regardless of the casing of the table names.

By making this change, the function will now pass all the provided failing test cases and satisfy the expected input/output values. This fix aligns with the reported GitHub issue titled "Fix #896: make table_exists case insensitive."